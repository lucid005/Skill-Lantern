ALTER TABLE "CareerRecommendation"
ADD COLUMN "roadmapProgress" JSONB,
ADD COLUMN "userFeedback" TEXT,
ADD COLUMN "feedbackComment" TEXT,
ADD COLUMN "feedbackCreatedAt" TIMESTAMP(3);
