"""
Gemini Service - Google Gemini API Integration
Handles all communication with the Gemini API for LLM inference.
"""

import ast
import json
import re
from typing import Optional, Dict, Any, AsyncGenerator
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class GeminiServiceError(Exception):
    """Structured Gemini API error with HTTP-like metadata."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 500,
        code: str = "GEMINI_ERROR",
        retry_after_seconds: Optional[int] = None,
        raw_error: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.retry_after_seconds = retry_after_seconds
        self.raw_error = raw_error or {}

    @property
    def is_quota_exhausted(self) -> bool:
        return self.status_code == 429 or self.code == "RESOURCE_EXHAUSTED"

    def __str__(self) -> str:
        if self.retry_after_seconds:
            return f"{self.message} Retry after {self.retry_after_seconds}s."
        return self.message


class GeminiService:
    """Service for interacting with Google Gemini API."""
    
    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.model = settings.gemini_model
        self.timeout = settings.gemini_timeout
        self._client = None
    
    def _get_client(self):
        """Lazy-initialize the Gemini client."""
        if self._client is None:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def _parse_error_payload(self, message: str) -> Dict[str, Any]:
        """Extract the provider payload from the exception string when available."""
        payload_start = message.find("{")
        if payload_start == -1:
            return {}

        payload_text = message[payload_start:]

        try:
            return json.loads(payload_text)
        except json.JSONDecodeError:
            try:
                return ast.literal_eval(payload_text)
            except (SyntaxError, ValueError):
                return {}

    def _extract_retry_after_seconds(self, message: str, payload: Dict[str, Any]) -> Optional[int]:
        """Extract retry delay from Gemini RetryInfo or fallback text parsing."""
        details = payload.get("error", {}).get("details", [])
        for detail in details:
            retry_delay = detail.get("retryDelay")
            if isinstance(retry_delay, str):
                match = re.search(r"(\d+)", retry_delay)
                if match:
                    return int(match.group(1))

        match = re.search(r"retry in\s+(\d+(?:\.\d+)?)s", message, flags=re.IGNORECASE)
        if match:
            return int(float(match.group(1)))

        return None

    def _normalize_error(self, error: Exception, operation: str) -> GeminiServiceError:
        """Convert raw Gemini exceptions into structured service errors."""
        message = str(error)
        payload = self._parse_error_payload(message)
        error_payload = payload.get("error", {})

        status_code = getattr(error, "status_code", None)
        if status_code is None:
            error_code_attr = getattr(error, "code", None)
            if isinstance(error_code_attr, int):
                status_code = error_code_attr

        if status_code is None and "429" in message:
            status_code = 429

        code = error_payload.get("status") or getattr(error, "status", None) or "GEMINI_ERROR"
        if status_code == 429 and code == "GEMINI_ERROR":
            code = "RESOURCE_EXHAUSTED"

        provider_message = error_payload.get("message") or message
        retry_after_seconds = self._extract_retry_after_seconds(message, payload)

        return GeminiServiceError(
            f"Gemini {operation} failed: {provider_message}",
            status_code=status_code or 500,
            code=code,
            retry_after_seconds=retry_after_seconds,
            raw_error=payload,
        )
        
    async def check_health(self) -> bool:
        """Check if Gemini API is accessible."""
        try:
            if not self.api_key:
                logger.error("Gemini API key is not configured")
                return False
            client = self._get_client()
            # List models to verify API key and connectivity
            models = client.models.list()
            # If we can iterate at least one model, the API is working
            for _ in models:
                return True
            return True
        except Exception as e:
            logger.error(f"Gemini health check failed: {e}")
            return False
    
    async def list_models(self) -> list:
        """List available models in Gemini."""
        try:
            client = self._get_client()
            models = client.models.list()
            return [m.name for m in models]
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.5,
        max_tokens: int = 1024
    ) -> str:
        """
        Generate text using Gemini API.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            temperature: Creativity parameter (0-1)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text response
        """
        try:
            from google.genai import types
            
            client = self._get_client()
            
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            if system_prompt:
                config.system_instruction = system_prompt
            
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )
            
            return response.text or ""
                    
        except Exception as e:
            normalized_error = self._normalize_error(e, "generate")
            logger.error("Gemini generate error: %s", normalized_error)
            raise normalized_error from e
    
    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """
        Generate text with streaming response.
        
        Yields:
            Text chunks as they are generated
        """
        try:
            from google.genai import types
            
            client = self._get_client()
            
            config = types.GenerateContentConfig(
                temperature=temperature,
            )
            
            if system_prompt:
                config.system_instruction = system_prompt
            
            response = client.models.generate_content_stream(
                model=self.model,
                contents=prompt,
                config=config
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            normalized_error = self._normalize_error(e, "stream")
            logger.error("Gemini stream error: %s", normalized_error)
            raise normalized_error from e
    
    async def chat(
        self,
        messages: list,
        temperature: float = 0.7
    ) -> str:
        """
        Chat completion using Gemini API.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Creativity parameter
            
        Returns:
            Assistant's response
        """
        try:
            from google.genai import types
            
            client = self._get_client()
            
            # Convert generic chat messages to Gemini content objects.
            # Gemini uses [types.Content(role="user", parts=[types.Part(text="...")])].
            gemini_contents = []
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                # Map 'assistant' role to 'model' for Gemini
                if role == "assistant":
                    role = "model"
                gemini_contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part(text=content)]
                    )
                )
            
            config = types.GenerateContentConfig(
                temperature=temperature,
            )
            
            response = client.models.generate_content(
                model=self.model,
                contents=gemini_contents,
                config=config
            )
            
            return response.text or ""
                    
        except Exception as e:
            normalized_error = self._normalize_error(e, "chat")
            logger.error("Gemini chat error: %s", normalized_error)
            raise normalized_error from e
    
    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON from LLM response.
        Handles cases where JSON is embedded in markdown or text.
        """
        # Try direct JSON parse
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown code blocks
        json_patterns = [
            r'```json\s*([\s\S]*?)\s*```',
            r'```\s*([\s\S]*?)\s*```',
            r'\{[\s\S]*\}'
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, response)
            for match in matches:
                try:
                    # Clean up the match
                    cleaned = match.strip()
                    if not cleaned.startswith('{'):
                        # Find the first { and last }
                        start = cleaned.find('{')
                        end = cleaned.rfind('}')
                        if start != -1 and end != -1:
                            cleaned = cleaned[start:end+1]
                    return json.loads(cleaned)
                except json.JSONDecodeError:
                    continue
        
        # Return raw response wrapped in dict if JSON parsing fails
        logger.warning("Could not parse JSON from LLM response, returning raw")
        return {"raw_response": response}


# Singleton instance
gemini_service = GeminiService()
