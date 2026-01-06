/**
 * Career-related TypeScript interfaces
 */

// Enums
export type EducationLevel = 'high_school' | 'plus_two' | 'bachelors' | 'masters' | 'phd';
export type DegreeLevel = 'diploma' | 'bachelors' | 'masters' | 'phd';
export type BudgetRange = 'low' | 'medium' | 'high';

// User Profile
export interface UserProfile {
  name?: string;
  gender?: string;
  education_level: EducationLevel;
  ug_course?: string;
  specialization?: string;
  skills: string[];
  interests: string[];
  preferences?: string;
  cgpa?: number;
  certifications: string[];
  location: string;
}

// Career Prediction
export interface PredictedCareer {
  career: string;
  confidence: number;
  description?: string;
}

export interface CareerPredictionRequest {
  user_profile: UserProfile;
}

export interface CareerPredictionResponse {
  predictions: PredictedCareer[];
  user_profile_summary: Record<string, unknown>;
  message: string;
}

// Roadmap
export interface RoadmapStage {
  level: string;
  duration: string;
  skills: string[];
  resources: string[];
  milestones: string[];
}

export interface RoadmapRequest {
  career_name: string;
  user_profile: UserProfile;
}

export interface RoadmapResponse {
  career: string;
  overview: string;
  stages: RoadmapStage[];
  tools_and_technologies: string[];
  job_roles: string[];
  growth_paths: string[];
  raw_response?: string;
}

// College
export interface CollegeInfo {
  name: string;
  location: string;
  university?: string;
  programs: string[];
  ownership_type?: string;
  phone?: string;
  email?: string;
  reason?: string;
}

export interface CollegeRequest {
  career_name: string;
  required_courses?: string[];
  preferred_location?: string;
  budget_range?: BudgetRange;
  degree_level?: DegreeLevel;
}

export interface CollegeRecommendationResponse {
  career: string;
  recommendations: CollegeInfo[];
  alternatives: CollegeInfo[];
  notes?: string;
  raw_response?: string;
}

// Full Recommendation
export interface FullRecommendationRequest {
  user_profile: UserProfile;
  preferred_location?: string;
  budget_range?: BudgetRange;
  degree_level?: DegreeLevel;
}

export interface FullRecommendationResponse {
  predicted_careers: PredictedCareer[];
  selected_career: string;
  roadmap: RoadmapResponse;
  colleges: CollegeRecommendationResponse;
  summary: string;
  immediate_actions: string[];
}

// Health
export interface HealthResponse {
  status: string;
  ollama_status: string;
  model_loaded: boolean;
  version: string;
}

// Error
export interface ErrorResponse {
  error: string;
  detail?: string;
  code?: string;
}
