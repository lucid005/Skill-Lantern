/**
 * useCareerPrediction Hook
 * React hook for career prediction functionality
 */

'use client';

import { useState, useCallback } from 'react';
import { predictCareer, getCareerCategories, getCareerInsights } from '../lib/api/career-api';
import { UserProfile, PredictedCareer } from '../lib/types/career';

interface UseCareerPredictionReturn {
  predictions: PredictedCareer[];
  loading: boolean;
  error: string | null;
  predict: (profile: UserProfile) => Promise<void>;
  fetchCategories: () => Promise<string[]>;
  fetchInsights: (career: string) => Promise<void>;
  insights: Record<string, unknown> | null;
  reset: () => void;
}

export function useCareerPrediction(): UseCareerPredictionReturn {
  const [predictions, setPredictions] = useState<PredictedCareer[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [insights, setInsights] = useState<Record<string, unknown> | null>(null);

  const predict = useCallback(async (profile: UserProfile) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await predictCareer({ user_profile: profile });
      setPredictions(response.predictions);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to predict career');
      setPredictions([]);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchCategories = useCallback(async () => {
    try {
      return await getCareerCategories();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch categories');
      return [];
    }
  }, []);

  const fetchInsights = useCallback(async (career: string) => {
    setLoading(true);
    try {
      const data = await getCareerInsights(career);
      setInsights(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch insights');
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setPredictions([]);
    setError(null);
    setInsights(null);
  }, []);

  return {
    predictions,
    loading,
    error,
    predict,
    fetchCategories,
    fetchInsights,
    insights,
    reset,
  };
}
