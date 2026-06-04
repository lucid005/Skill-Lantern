import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import bcrypt from 'bcryptjs';

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const {
            email,
            password,
            fullName,
            gender,
            dateOfBirth,
            cityRegion,
            courseCategory,
            course,
            specialization,
            schoolCollegeName,
            cgpa,
            interests,
            technicalSkills,
            softSkills,
            hasCertification,
            certifications,
            careerLifestyle,
            workEnvironment,
            locationPreference,
            learningStyle,
        } = body;

        // Validate required fields
        if (!email || !password) {
            return NextResponse.json(
                { error: 'Email and password are required' },
                { status: 400 }
            );
        }

        if (typeof email !== 'string' || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            return NextResponse.json(
                { error: 'Please enter a valid email address' },
                { status: 400 }
            );
        }

        if (typeof password !== 'string' || password.length < 8) {
            return NextResponse.json(
                { error: 'Password must be at least 8 characters long' },
                { status: 400 }
            );
        }

        if (body.confirmPassword !== undefined && password !== body.confirmPassword) {
            return NextResponse.json(
                { error: 'Passwords do not match' },
                { status: 400 }
            );
        }

        // Check if user already exists
        const existingUser = await prisma.user.findUnique({
            where: { email },
        });

        if (existingUser) {
            return NextResponse.json(
                { error: 'An account with this email already exists' },
                { status: 409 }
            );
        }

        // Hash password
        const hashedPassword = await bcrypt.hash(password, 12);

        // Parse CGPA
        let parsedCgpa: number | null = null;
        if (cgpa) {
            const cleaned = cgpa.replace('%', '').trim();
            const num = parseFloat(cleaned);
            if (!isNaN(num)) {
                parsedCgpa = num;
            }
        }

        // Parse date of birth
        let parsedDob: Date | null = null;
        if (dateOfBirth) {
            parsedDob = new Date(dateOfBirth);
            if (isNaN(parsedDob.getTime())) {
                parsedDob = null;
            }
        }

        // Create user and profile in a transaction
        const user = await prisma.user.create({
            data: {
                email,
                name: fullName || null,
                password: hashedPassword,
                profile: {
                    create: {
                        fullName: fullName || null,
                        gender: gender || null,
                        dateOfBirth: parsedDob,
                        cityRegion: cityRegion || null,
                        courseCategory: courseCategory || null,
                        course: course || null,
                        specialization: specialization || null,
                        schoolCollegeName: schoolCollegeName || null,
                        cgpa: parsedCgpa,
                        interests: interests || [],
                        technicalSkills: technicalSkills || [],
                        softSkills: softSkills || [],
                        hasCertification: hasCertification || false,
                        certifications: certifications || null,
                        careerLifestyle: careerLifestyle || null,
                        workEnvironment: workEnvironment || null,
                        locationPreference: locationPreference || null,
                        learningStyle: learningStyle || null,
                    },
                },
            },
            select: {
                id: true,
                email: true,
                name: true,
            },
        });

        return NextResponse.json(
            { success: true, user },
            { status: 201 }
        );
    } catch (error) {
        console.error('Signup error:', error);
        return NextResponse.json(
            { error: 'Failed to create account. Please try again.' },
            { status: 500 }
        );
    }
}
