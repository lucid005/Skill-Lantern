/**
 * Recommendations API Client
 * Handles full career recommendation API calls
 */

import {
  FullRecommendationRequest,
  FullRecommendationResponse,
  CollegeRequest,
  CollegeRecommendationResponse,
  HealthResponse,
  CareerPredictionRequest,
} from '../types/career';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Get complete career recommendation
 */
export async function getFullRecommendation(
  request: FullRecommendationRequest
): Promise<FullRecommendationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/recommendations/full`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get recommendations');
  }

  return response.json();
}

/**
 * Get quick career recommendation (faster, less detailed)
 */
export async function getQuickRecommendation(
  request: CareerPredictionRequest
): Promise<{
  predictions: Array<{
    career: string;
    confidence: number;
    description?: string;
  }>;
  top_career: string;
  insights: Record<string, unknown>;
  message: string;
}> {
  const response = await fetch(`${API_BASE_URL}/api/recommendations/quick`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get quick recommendation');
  }

  return response.json();
}

/**
 * Get college recommendations
 */
export async function getCollegeRecommendations(
  request: CollegeRequest
): Promise<CollegeRecommendationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/colleges/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get college recommendations');
  }

  return response.json();
}

/**
 * List colleges with optional filters
 */
export async function listColleges(params?: {
  location?: string;
  program?: string;
  university?: string;
  limit?: number;
}): Promise<{
  total: number;
  colleges: Array<{
    name: string;
    location: string;
    university: string;
    programs: string;
    ownership_type: string;
    phone: string;
    email: string;
  }>;
}> {
  const searchParams = new URLSearchParams();
  if (params?.location) searchParams.set('location', params.location);
  if (params?.program) searchParams.set('program', params.program);
  if (params?.university) searchParams.set('university', params.university);
  if (params?.limit) searchParams.set('limit', params.limit.toString());

  const response = await fetch(
    `${API_BASE_URL}/api/colleges/list?${searchParams.toString()}`
  );

  if (!response.ok) {
    throw new Error('Failed to list colleges');
  }

  return response.json();
}

/**
 * Get list of locations
 */
export async function getLocations(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/api/colleges/locations`);

  if (!response.ok) {
    throw new Error('Failed to get locations');
  }

  return response.json();
}

/**
 * Get list of universities
 */
export async function getUniversities(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/api/colleges/universities`);

  if (!response.ok) {
    throw new Error('Failed to get universities');
  }

  return response.json();
}

/**
 * Check API health status
 */
export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/health`);

  if (!response.ok) {
    throw new Error('API is not healthy');
  }

  return response.json();
}

/**
 * Stream full recommendation generation
 */
export async function* streamFullRecommendation(
  request: FullRecommendationRequest
): AsyncGenerator<
  {
    step: string;
    message?: string;
    careers?: Array<{ career: string; confidence: number }>;
    data?: FullRecommendationResponse;
    error?: string;
  },
  void,
  unknown
> {
  const response = await fetch(`${API_BASE_URL}/api/recommendations/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error('Failed to start recommendation stream');
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
          yield JSON.parse(data);
        } catch {
          // Skip invalid JSON
        }
      }
    }
  }
}
