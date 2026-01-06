/**
 * useRecommendations Hook
 * React hook for full career recommendations
 */

'use client';

import { useState, useCallback } from 'react';
import {
  getFullRecommendation,
  getQuickRecommendation,
  streamFullRecommendation,
  checkHealth,
} from '../lib/api/recommendations-api';
import {
  UserProfile,
  FullRecommendationResponse,
  FullRecommendationRequest,
  HealthResponse,
} from '../lib/types/career';

interface UseRecommendationsReturn {
  recommendation: FullRecommendationResponse | null;
  loading: boolean;
  error: string | null;
  progress: string;
  getRecommendation: (request: FullRecommendationRequest) => Promise<void>;
  getQuick: (profile: UserProfile) => Promise<void>;
  streamRecommendation: (request: FullRecommendationRequest) => Promise<void>;
  checkApiHealth: () => Promise<HealthResponse | null>;
  reset: () => void;
}

export function useRecommendations(): UseRecommendationsReturn {
  const [recommendation, setRecommendation] = useState<FullRecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<string>('');

  const getRecommendation = useCallback(async (request: FullRecommendationRequest) => {
    setLoading(true);
    setError(null);
    setProgress('Generating recommendations...');
    
    try {
      const response = await getFullRecommendation(request);
      setRecommendation(response);
      setProgress('Complete!');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get recommendations');
      setRecommendation(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const getQuick = useCallback(async (profile: UserProfile) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await getQuickRecommendation({ user_profile: profile });
      // Convert quick response to partial full recommendation
      setRecommendation({
        predicted_careers: response.predictions.map(p => ({
          career: p.career,
          confidence: p.confidence,
          description: p.description,
        })),
        selected_career: response.top_career,
        roadmap: {
          career: response.top_career,
          overview: '',
          stages: [],
          tools_and_technologies: [],
          job_roles: [],
          growth_paths: [],
        },
        colleges: {
          career: response.top_career,
          recommendations: [],
          alternatives: [],
        },
        summary: response.message,
        immediate_actions: [],
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get quick recommendation');
    } finally {
      setLoading(false);
    }
  }, []);

  const streamRecommendation = useCallback(async (request: FullRecommendationRequest) => {
    setLoading(true);
    setError(null);
    setProgress('Starting...');
    
    try {
      for await (const update of streamFullRecommendation(request)) {
        if (update.error) {
          throw new Error(update.error);
        }
        
        if (update.message) {
          setProgress(update.message);
        }
        
        if (update.step === 'complete' && update.data) {
          setRecommendation(update.data);
        }
      }
      setProgress('Complete!');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Streaming failed');
    } finally {
      setLoading(false);
    }
  }, []);

  const checkApiHealth = useCallback(async () => {
    try {
      return await checkHealth();
    } catch {
      return null;
    }
  }, []);

  const reset = useCallback(() => {
    setRecommendation(null);
    setError(null);
    setProgress('');
  }, []);

  return {
    recommendation,
    loading,
    error,
    progress,
    getRecommendation,
    getQuick,
    streamRecommendation,
    checkApiHealth,
    reset,
  };
}
