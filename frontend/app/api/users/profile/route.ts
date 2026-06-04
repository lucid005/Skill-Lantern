import { NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { prisma } from '@/lib/db';

function toStringArray(value: unknown): string[] {
    if (!Array.isArray(value)) return [];
    return value
        .map((item) => String(item).trim())
        .filter(Boolean)
        .slice(0, 30);
}

function parseCgpa(value: unknown): number | null {
    if (value === null || value === undefined || value === '') return null;
    const parsed = Number(String(value).replace('%', '').trim());
    if (!Number.isFinite(parsed)) return null;
    return Math.min(Math.max(parsed, 0), 100);
}

function profileResponse(profile: {
    fullName: string | null;
    course: string | null;
    specialization: string | null;
    interests: string[];
    technicalSkills: string[];
    softSkills: string[];
    courseCategory: string | null;
    schoolCollegeName: string | null;
    cgpa: number | null;
    gender: string | null;
    cityRegion: string | null;
    careerLifestyle: string | null;
    workEnvironment: string | null;
    locationPreference: string | null;
    learningStyle: string | null;
    hasCertification: boolean;
    certifications: string | null;
}) {
    return {
        fullName: profile.fullName,
        course: profile.course,
        specialization: profile.specialization,
        interests: profile.interests,
        technicalSkills: profile.technicalSkills,
        softSkills: profile.softSkills,
        courseCategory: profile.courseCategory,
        schoolCollegeName: profile.schoolCollegeName,
        cgpa: profile.cgpa,
        gender: profile.gender,
        cityRegion: profile.cityRegion,
        careerLifestyle: profile.careerLifestyle,
        workEnvironment: profile.workEnvironment,
        locationPreference: profile.locationPreference,
        learningStyle: profile.learningStyle,
        hasCertification: profile.hasCertification,
        certifications: profile.certifications,
    };
}

export async function GET() {
    try {
        const session = await auth();

        if (!session?.user?.id) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            );
        }

        const profile = await prisma.userProfile.findUnique({
            where: { userId: session.user.id },
        });

        if (!profile) {
            return NextResponse.json(
                { error: 'Profile not found' },
                { status: 404 }
            );
        }

        return NextResponse.json(profileResponse(profile));
    } catch (error) {
        console.error('Error fetching profile:', error);
        return NextResponse.json(
            { error: 'Failed to fetch profile' },
            { status: 500 }
        );
    }
}

export async function PATCH(request: Request) {
    try {
        const session = await auth();

        if (!session?.user?.id) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            );
        }

        const body = await request.json();
        const profile = await prisma.userProfile.upsert({
            where: { userId: session.user.id },
            create: {
                userId: session.user.id,
                fullName: typeof body.fullName === 'string' ? body.fullName.trim() || null : null,
                course: typeof body.course === 'string' ? body.course.trim() || null : null,
                specialization: typeof body.specialization === 'string' ? body.specialization.trim() || null : null,
                interests: toStringArray(body.interests),
                technicalSkills: toStringArray(body.technicalSkills),
                softSkills: toStringArray(body.softSkills),
                cgpa: parseCgpa(body.cgpa),
                cityRegion: typeof body.cityRegion === 'string' ? body.cityRegion.trim() || null : null,
                careerLifestyle: typeof body.careerLifestyle === 'string' ? body.careerLifestyle.trim() || null : null,
                workEnvironment: typeof body.workEnvironment === 'string' ? body.workEnvironment.trim() || null : null,
                locationPreference: typeof body.locationPreference === 'string' ? body.locationPreference.trim() || null : null,
                learningStyle: typeof body.learningStyle === 'string' ? body.learningStyle.trim() || null : null,
            },
            update: {
                fullName: typeof body.fullName === 'string' ? body.fullName.trim() || null : undefined,
                course: typeof body.course === 'string' ? body.course.trim() || null : undefined,
                specialization: typeof body.specialization === 'string' ? body.specialization.trim() || null : undefined,
                interests: Array.isArray(body.interests) ? toStringArray(body.interests) : undefined,
                technicalSkills: Array.isArray(body.technicalSkills) ? toStringArray(body.technicalSkills) : undefined,
                softSkills: Array.isArray(body.softSkills) ? toStringArray(body.softSkills) : undefined,
                cgpa: body.cgpa !== undefined ? parseCgpa(body.cgpa) : undefined,
                cityRegion: typeof body.cityRegion === 'string' ? body.cityRegion.trim() || null : undefined,
                careerLifestyle: typeof body.careerLifestyle === 'string' ? body.careerLifestyle.trim() || null : undefined,
                workEnvironment: typeof body.workEnvironment === 'string' ? body.workEnvironment.trim() || null : undefined,
                locationPreference: typeof body.locationPreference === 'string' ? body.locationPreference.trim() || null : undefined,
                learningStyle: typeof body.learningStyle === 'string' ? body.learningStyle.trim() || null : undefined,
            },
        });

        return NextResponse.json(profileResponse(profile));
    } catch (error) {
        console.error('Error updating profile:', error);
        return NextResponse.json(
            { error: 'Failed to update profile' },
            { status: 500 }
        );
    }
}
