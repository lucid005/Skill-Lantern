import { NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { prisma } from '@/lib/db';

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

        return NextResponse.json({
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
        });
    } catch (error) {
        console.error('Error fetching profile:', error);
        return NextResponse.json(
            { error: 'Failed to fetch profile' },
            { status: 500 }
        );
    }
}
