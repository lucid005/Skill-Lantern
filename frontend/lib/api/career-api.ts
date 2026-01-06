/**
 * Career API Client
 * Handles all career-related API calls to the backend
 */

import {
  CareerPredictionRequest,
  CareerPredictionResponse,
} from '../types/career';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Predict careers based on user profile
 */
export async function predictCareer(
  request: CareerPredictionRequest
): Promise<CareerPredictionResponse> {
  const response = await fetch(`${API_BASE_URL}/api/career/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to predict career');
  }

  return response.json();
}

/**
 * Get list of career categories
 */
export async function getCareerCategories(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/api/career/categories`);

  if (!response.ok) {
    throw new Error('Failed to fetch career categories');
  }

  return response.json();
}

/**
 * Get insights about a specific career
 */
export async function getCareerInsights(careerName: string): Promise<{
  career: string;
  description: string;
  common_skills: string[];
  growth_outlook: string;
}> {
  const response = await fetch(
    `${API_BASE_URL}/api/career/insights/${encodeURIComponent(careerName)}`
  );

  if (!response.ok) {
    throw new Error('Failed to fetch career insights');
  }

  return response.json();
}
