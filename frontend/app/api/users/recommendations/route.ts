import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { prisma } from '@/lib/db';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

type RecommendationRecord = Awaited<ReturnType<typeof prisma.careerRecommendation.findFirst>>;

function serializeRecommendation(recommendation: NonNullable<RecommendationRecord>) {
    return {
        id: recommendation.id,
        predictions: recommendation.predictions,
        topCareer: recommendation.topCareer,
        hasFullDetails: recommendation.hasFullDetails,
        roadmap: recommendation.roadmap,
        colleges: recommendation.colleges,
        summary: recommendation.summary,
        immediateActions: recommendation.immediateActions,
        roadmapProgress: recommendation.roadmapProgress,
        userFeedback: recommendation.userFeedback,
        feedbackComment: recommendation.feedbackComment,
        feedbackCreatedAt: recommendation.feedbackCreatedAt?.toISOString() ?? null,
        createdAt: recommendation.createdAt.toISOString(),
    };
}

// Helper: Map DB profile to backend UserProfile format
function mapProfileToBackendFormat(profile: {
    fullName: string | null;
    gender: string | null;
    course: string | null;
    courseCategory: string | null;
    specialization: string | null;
    interests: string[];
    technicalSkills: string[];
    softSkills: string[];
    cgpa: number | null;
    certifications: string | null;
    hasCertification: boolean;
    careerLifestyle: string | null;
    workEnvironment: string | null;
    locationPreference: string | null;
    cityRegion: string | null;
}) {
    // Map courseCategory to education_level
    const educationLevelMap: Record<string, string> = {
        engineering: 'bachelors',
        science: 'bachelors',
        commerce: 'bachelors',
        business: 'bachelors',
        computer: 'bachelors',
        arts: 'bachelors',
        law: 'bachelors',
        medical: 'bachelors',
        media: 'bachelors',
        architecture: 'bachelors',
        hospitality: 'bachelors',
        other: 'bachelors',
    };

    const allSkills = [...(profile.technicalSkills || []), ...(profile.softSkills || [])];

    // Build preferences string from lifestyle/work preferences
    const prefParts = [
        profile.careerLifestyle,
        profile.workEnvironment,
        profile.locationPreference,
    ].filter(Boolean);

    const certList = profile.hasCertification && profile.certifications
        ? profile.certifications.split(',').map(c => c.trim()).filter(Boolean)
        : [];

    return {
        name: profile.fullName || undefined,
        gender: profile.gender || undefined,
        education_level: educationLevelMap[profile.courseCategory || ''] || 'bachelors',
        ug_course: profile.course || undefined,
        specialization: profile.specialization || undefined,
        skills: allSkills,
        interests: profile.interests || [],
        preferences: prefParts.length > 0 ? prefParts.join(', ') : undefined,
        cgpa: profile.cgpa || undefined,
        certifications: certList,
        location: profile.cityRegion || 'Nepal',
    };
}

// GET - Fetch latest recommendation or full recommendation history for the authenticated user
export async function GET(request: NextRequest) {
    try {
        const session = await auth();
        if (!session?.user?.id) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const includeAll = request.nextUrl.searchParams.get('all') === 'true';

        if (includeAll) {
            const recommendations = await prisma.careerRecommendation.findMany({
                where: { userId: session.user.id },
                orderBy: { createdAt: 'desc' },
            });

            return NextResponse.json(recommendations.map(serializeRecommendation));
        }

        const recommendation = await prisma.careerRecommendation.findFirst({
            where: { userId: session.user.id },
            orderBy: { createdAt: 'desc' },
        });

        if (!recommendation) {
            return NextResponse.json(null);
        }

        return NextResponse.json(serializeRecommendation(recommendation));
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        return NextResponse.json(
            { error: 'Failed to fetch recommendations' },
            { status: 500 }
        );
    }
}

// POST - Call AI backend and save recommendation
export async function POST() {
    try {
        const session = await auth();
        if (!session?.user?.id) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        // Fetch the user's profile
        const profile = await prisma.userProfile.findUnique({
            where: { userId: session.user.id },
        });

        if (!profile) {
            return NextResponse.json(
                { error: 'Profile not found. Please complete your profile first.' },
                { status: 404 }
            );
        }

        // Map profile to backend format
        const backendProfile = mapProfileToBackendFormat(profile);

        // Call the FastAPI backend
        const backendResponse = await fetch(`${API_BASE_URL}/api/recommendations/full`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_profile: backendProfile,
                preferred_location: profile.cityRegion || undefined,
                degree_level: 'bachelors',
            }),
        });

        if (!backendResponse.ok) {
            const errorData = await backendResponse.json().catch(() => ({}));
            console.error('Backend error:', errorData);
            throw new Error(errorData.detail || 'AI backend request failed');
        }

        const aiResult = await backendResponse.json();

        // Save to database
        const recommendation = await prisma.careerRecommendation.create({
            data: {
                userId: session.user.id,
                predictions: aiResult.predicted_careers || [],
                topCareer: aiResult.selected_career || aiResult.predicted_careers?.[0]?.career || null,
                roadmap: aiResult.roadmap || null,
                colleges: aiResult.colleges || null,
                summary: aiResult.summary || null,
                immediateActions: aiResult.immediate_actions || [],
                hasFullDetails: !!(aiResult.roadmap && aiResult.colleges),
            },
        });

        return NextResponse.json(serializeRecommendation(recommendation));
    } catch (error) {
        console.error('Error generating recommendations:', error);
        const message = error instanceof Error ? error.message : 'Failed to generate recommendations';
        return NextResponse.json(
            { error: message },
            { status: 500 }
        );
    }
}

// PATCH - Get full details for an existing recommendation
export async function PATCH(request: Request) {
    try {
        const session = await auth();
        if (!session?.user?.id) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const body = await request.json();
        const { recommendationId, action } = body;

        if (!recommendationId) {
            return NextResponse.json(
                { error: 'Recommendation ID is required' },
                { status: 400 }
            );
        }

        // Fetch existing recommendation
        const existing = await prisma.careerRecommendation.findFirst({
            where: { id: recommendationId, userId: session.user.id },
        });

        if (!existing) {
            return NextResponse.json(
                { error: 'Recommendation not found' },
                { status: 404 }
            );
        }

        if (action === 'feedback') {
            const feedback = body.userFeedback === 'helpful' || body.userFeedback === 'not_helpful'
                ? body.userFeedback
                : null;

            if (!feedback) {
                return NextResponse.json(
                    { error: 'Feedback must be helpful or not_helpful' },
                    { status: 400 }
                );
            }

            const updated = await prisma.careerRecommendation.update({
                where: { id: recommendationId },
                data: {
                    userFeedback: feedback,
                    feedbackComment: typeof body.feedbackComment === 'string'
                        ? body.feedbackComment.trim().slice(0, 1000) || null
                        : null,
                    feedbackCreatedAt: new Date(),
                },
            });

            return NextResponse.json(serializeRecommendation(updated));
        }

        if (action === 'roadmap_progress') {
            const progress = body.roadmapProgress && typeof body.roadmapProgress === 'object'
                ? body.roadmapProgress
                : {};

            const updated = await prisma.careerRecommendation.update({
                where: { id: recommendationId },
                data: {
                    roadmapProgress: progress,
                },
            });

            return NextResponse.json(serializeRecommendation(updated));
        }

        // If already has full details, just return it
        if (existing.hasFullDetails) {
            return NextResponse.json(serializeRecommendation(existing));
        }

        // Fetch user profile for the AI call
        const profile = await prisma.userProfile.findUnique({
            where: { userId: session.user.id },
        });

        if (!profile) {
            return NextResponse.json(
                { error: 'Profile not found' },
                { status: 404 }
            );
        }

        const backendProfile = mapProfileToBackendFormat(profile);

        // Call backend for full recommendation
        const backendResponse = await fetch(`${API_BASE_URL}/api/recommendations/full`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_profile: backendProfile,
                preferred_location: profile.cityRegion || undefined,
                degree_level: 'bachelors',
            }),
        });

        if (!backendResponse.ok) {
            throw new Error('Failed to get full details from AI backend');
        }

        const aiResult = await backendResponse.json();

        // Update the recommendation with full details
        const updated = await prisma.careerRecommendation.update({
            where: { id: recommendationId },
            data: {
                roadmap: aiResult.roadmap || null,
                colleges: aiResult.colleges || null,
                summary: aiResult.summary || null,
                immediateActions: aiResult.immediate_actions || [],
                hasFullDetails: true,
            },
        });

        return NextResponse.json(serializeRecommendation(updated));
    } catch (error) {
        console.error('Error getting full details:', error);
        return NextResponse.json(
            { error: 'Failed to get full details' },
            { status: 500 }
        );
    }
}
