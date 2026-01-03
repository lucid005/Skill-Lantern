"use client";

import Link from "next/link";
import { MotionSection, MotionStagger } from "@/components/MotionAnimations";

export default function Features() {
  const mainFeatures = [
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      ),
      title: "AI-Powered Career Matching",
      description: "Our advanced machine learning algorithms analyze your complete profile—skills, education, interests, and goals—to match you with the most suitable career paths from our database of 10,000+ careers.",
      benefits: [
        "XGBoost-powered prediction engine",
        "Multi-factor profile analysis",
        "Confidence scores for each recommendation",
        "Continuous learning from user feedback",
      ],
    },
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      ),
      title: "Comprehensive Skill Gap Analysis",
      description: "Identify exactly what skills you need to develop to succeed in your chosen career. Our platform maps your current abilities against industry requirements and shows you the path forward.",
      benefits: [
        "Real-time skill assessment",
        "Industry-standard benchmarking",
        "Priority-ranked skill gaps",
        "Progress tracking over time",
      ],
    },
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
      ),
      title: "Personalized Learning Roadmaps",
      description: "Get step-by-step learning paths customized for your recommended careers. Each roadmap includes curated courses, certifications, projects, and milestones to track your progress.",
      benefits: [
        "Curated course recommendations",
        "Certification guidance",
        "Hands-on project suggestions",
        "Timeline-based milestones",
      ],
    },
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
      ),
      title: "Real-Time Market Insights",
      description: "Make informed decisions with up-to-date job market data. Understand salary ranges, growth projections, demand trends, and industry dynamics for every career path.",
      benefits: [
        "Salary benchmarking data",
        "Job market demand analysis",
        "Industry growth projections",
        "Geographic opportunity mapping",
      ],
    },
  ];

  const additionalFeatures = [
    {
      icon: "🎯",
      title: "Precision Matching",
      description: "95% accuracy in career recommendations based on comprehensive profile analysis.",
    },
    {
      icon: "🔒",
      title: "Data Privacy",
      description: "Your data is encrypted and never shared with third parties.",
    },
    {
      icon: "📊",
      title: "Progress Dashboard",
      description: "Track your career development journey with visual analytics.",
    },
    {
      icon: "🌐",
      title: "50+ Industries",
      description: "Comprehensive coverage across all major industry sectors.",
    },
    {
      icon: "📱",
      title: "Mobile Friendly",
      description: "Access your career insights anytime, anywhere on any device.",
    },
    {
      icon: "🔄",
      title: "Continuous Updates",
      description: "Regular updates with new careers and market data.",
    },
  ];

  return (
    <main className="flex flex-col pt-20 overflow-hidden">
      {/* Hero Section */}
      <section className="section-padding">
        <div className="container-custom text-center">
          <MotionSection className="max-w-3xl mx-auto">
            <div className="badge mb-6">Platform Features</div>
            <h1 className="text-4xl md:text-5xl font-semibold mb-6">
              Everything You Need to
              <br />
              <span className="gradient-text">Find Your Career Path</span>
            </h1>
            <p className="text-lg text-neutral-600 leading-relaxed">
              Skill Lantern combines cutting-edge AI technology with comprehensive career data to deliver personalized guidance that helps you make confident career decisions.
            </p>
          </MotionSection>
        </div>
      </section>

      {/* Main Features */}
      <section className="section-padding bg-neutral-50">
        <div className="container-custom">
          <div className="space-y-24">
            {mainFeatures.map((feature, index) => (
              <MotionSection
                key={index}
                animation={index % 2 === 0 ? "fade-right" : "fade-left"}
                className={`grid lg:grid-cols-2 gap-12 items-center ${index % 2 === 1 ? "lg:flex-row-reverse" : ""}`}
              >
                  <div className="w-16 h-16 bg-neutral-900 text-white rounded-2xl flex items-center justify-center mb-6 hover:scale-110 transition-transform">
                    {feature.icon}
                  </div>
                  <h2 className="text-2xl md:text-3xl font-semibold mb-4">
                    {feature.title}
                  </h2>
                  <p className="text-neutral-600 leading-relaxed mb-6">
                    {feature.description}
                  </p>
                  <ul className="space-y-3">
                    {feature.benefits.map((benefit, idx) => (
                      <li key={idx} className="flex items-center gap-3 hover:translate-x-1 transition-transform">
                        <svg
                          className="w-5 h-5 text-neutral-700"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                        <span className="text-neutral-700">{benefit}</span>
                      </li>
                    ))}
                  </ul>

                  <div className="aspect-video bg-neutral-100 rounded-xl flex items-center justify-center">
                    <div className="text-neutral-400 text-center">
                      <div className="w-16 h-16 bg-neutral-200 rounded-full flex items-center justify-center mx-auto mb-4">
                        {feature.icon}
                      </div>
                      <p className="text-sm">Feature Preview</p>
                    </div>
                  </div>
              </MotionSection>
            ))}
          </div>
        </div>
      </section>

      {/* Additional Features Grid */}
      <section className="section-padding">
        <div className="container-custom">
          <MotionSection className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-semibold mb-4">
              And Much More
            </h2>
            <p className="text-neutral-600 max-w-2xl mx-auto">
              Discover all the tools and features designed to help you succeed in your career journey.
            </p>
          </MotionSection>

          <MotionStagger className="grid md:grid-cols-2 lg:grid-cols-3 gap-8" stagger={0.08}>
            {additionalFeatures.map((feature, index) => (
              <div
                key={index}
                className="bg-neutral-50 p-8 rounded-2xl hover-lift"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-neutral-600">{feature.description}</p>
              </div>
            ))}
          </MotionStagger>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-neutral-900 text-white">
        <div className="container-custom text-center">
          <MotionSection animation="scale" className="max-w-2xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-semibold mb-6">
              Ready to Explore These Features?
            </h2>
            <p className="text-neutral-400 mb-8">
              Start your free career assessment today and experience the power of AI-driven career guidance.
            </p>
            <Link
              href="/registration/login"
              className="inline-flex items-center gap-2 bg-white text-neutral-900 px-8 py-4 rounded-lg font-medium hover:bg-neutral-100 hover:scale-105 transition-all btn-press"
            >
              Get Started Free
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17 8l4 4m0 0l-4 4m4-4H3"
                />
              </svg>
            </Link>
          </MotionSection>
        </div>
      </section>
    </main>
  );
}
