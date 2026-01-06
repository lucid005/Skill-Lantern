/**
 * Roadmap API Client
 * Handles career roadmap generation API calls
 */

import { RoadmapRequest, RoadmapResponse } from '../types/career';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Generate a career roadmap
 */
export async function generateRoadmap(
  request: RoadmapRequest
): Promise<RoadmapResponse> {
  const response = await fetch(`${API_BASE_URL}/api/roadmap/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to generate roadmap');
  }

  return response.json();
}

/**
 * Generate roadmap with streaming response
 * Returns an async generator that yields text chunks
 */
export async function* generateRoadmapStream(
  request: RoadmapRequest
): AsyncGenerator<string, void, unknown> {
  const response = await fetch(`${API_BASE_URL}/api/roadmap/generate/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error('Failed to start roadmap generation');
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error('No response body');
  }

  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6);
        if (data === '[DONE]') {
          return;
        }
        try {
          const parsed = JSON.parse(data);
          if (parsed.text) {
            yield parsed.text;
          }
          if (parsed.error) {
            throw new Error(parsed.error);
          }
        } catch {
          // Skip invalid JSON
        }
      }
    }
  }
}
