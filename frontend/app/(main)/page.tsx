"use client";

import Link from "next/link";
import { MotionSection, MotionStagger } from "@/components/MotionAnimations";

export default function Home() {
  const features = [
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      ),
      title: "AI-Powered Analysis",
      description: "Our advanced machine learning algorithms analyze your skills, interests, and academic background to generate personalized career recommendations.",
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      ),
      title: "Skill Gap Analysis",
      description: "Identify the exact skills you need to develop and get a clear roadmap to bridge the gap between where you are and where you want to be.",
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
      ),
      title: "Learning Roadmaps",
      description: "Get structured, step-by-step learning paths with curated courses, certifications, and resources tailored to your recommended career.",
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
      ),
      title: "Market Insights",
      description: "Access real-time job market data, salary ranges, growth projections, and demand trends for your recommended career paths.",
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      ),
      title: "Personalized Guidance",
      description: "Every recommendation is tailored to your unique profile—no generic advice. We consider your strengths, goals, and aspirations.",
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
      ),
      title: "Data Privacy",
      description: "Your data is secure and private. We use advanced encryption and never share your personal information with third parties.",
    },
  ];

  const steps = [
    {
      number: "01",
      title: "Complete Your Profile",
      description: "Tell us about your academic background, skills, interests, and career aspirations through our comprehensive assessment.",
    },
    {
      number: "02",
      title: "AI Analysis",
      description: "Our machine learning models analyze your profile against thousands of career paths and industry requirements.",
    },
    {
      number: "03",
      title: "Get Recommendations",
      description: "Receive personalized career recommendations with detailed insights, skill requirements, and growth potential.",
    },
    {
      number: "04",
      title: "Follow Your Roadmap",
      description: "Access your customized learning path with courses, certifications, and resources to achieve your career goals.",
    },
  ];

  const stats = [
    { value: "10K+", label: "Career Paths Analyzed" },
    { value: "95%", label: "Recommendation Accuracy" },
    { value: "50+", label: "Industries Covered" },
    { value: "24/7", label: "AI-Powered Support" },
  ];

  return (
    <main className="flex flex-col overflow-hidden">
      {/* Hero Section */}
      <section id="hero" className="min-h-screen flex items-center justify-center section-padding pt-32 md:pt-40">
        <div className="container-custom text-center">
          <div className="max-w-4xl mx-auto">
            <MotionSection animation="fade-down" duration={0.6}>
              <div className="badge mb-6">
                <span className="mr-2">✨</span>
                AI-Powered Career Recommendations
              </div>
            </MotionSection>
            
            <MotionSection animation="fade-up" duration={0.8} delay={0.1}>
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-semibold tracking-tight leading-tight mb-6">
                Discover Your Perfect
                <br />
                <span className="gradient-text">Career Path</span>
              </h1>
            </MotionSection>
            
            <MotionSection animation="fade-up" duration={0.8} delay={0.2}>
              <p className="text-lg md:text-xl text-neutral-600 max-w-2xl mx-auto mb-10 leading-relaxed">
                Skill Lantern uses advanced AI to analyze your skills, interests, and academic background to recommend the ideal career path tailored just for you.
              </p>
            </MotionSection>
            
            <MotionSection animation="fade-up" duration={0.8} delay={0.3}>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/registration/login" className="btn-primary btn-press text-base px-8 py-4 hover-lift">
                  Get Started Free
                </Link>
                <Link href="#how-it-works" className="btn-secondary btn-press text-base px-8 py-4">
                  See How It Works
                </Link>
              </div>
            </MotionSection>
          </div>

          {/* Stats Section */}
          <MotionStagger className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-20 pt-20 border-t border-neutral-200" stagger={0.1}>
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-3xl md:text-4xl font-semibold mb-2">{stat.value}</div>
                <div className="text-sm text-neutral-500">{stat.label}</div>
              </div>
            ))}
          </MotionStagger>
        </div>
      </section>

      {/* About Section */}
      <section className="section-padding bg-neutral-50" id="about">
        <div className="container-custom">
          <MotionSection className="max-w-3xl mx-auto text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-semibold mb-6">
              Why Skill Lantern?
            </h2>
            <p className="text-lg text-neutral-600 leading-relaxed">
              Students today don&apos;t just need information — they need personalized guidance that understands their individual strengths. Skill Lantern combines smart technology with real educational context to deliver meaningful career recommendations.
            </p>
          </MotionSection>

          <MotionStagger className="grid md:grid-cols-2 lg:grid-cols-3 gap-8" stagger={0.08}>
            {features.map((feature, index) => (
              <div
                key={index}
                className="bg-white p-8 rounded-2xl border border-neutral-200 hover-lift"
              >
                <div className="w-12 h-12 bg-neutral-100 rounded-xl flex items-center justify-center mb-6 text-neutral-700">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold mb-3">{feature.title}</h3>
                <p className="text-neutral-600 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </MotionStagger>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="section-padding" id="how-it-works">
        <div className="container-custom">
          <MotionSection className="max-w-3xl mx-auto text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-semibold mb-6">
              How It Works
            </h2>
            <p className="text-lg text-neutral-600 leading-relaxed">
              Getting your personalized career recommendation is simple. Follow these four easy steps to discover your ideal career path.
            </p>
          </MotionSection>

          <MotionStagger className="grid md:grid-cols-2 lg:grid-cols-4 gap-8" stagger={0.12}>
            {steps.map((step, index) => (
              <div key={index} className="relative group bg-inherit">
                <div className="text-6xl font-bold text-neutral-200 mb-4 group-hover:text-neutral-300 transition-colors">
                  {step.number}
                </div>
                <h3 className="text-lg font-semibold mb-3">{step.title}</h3>
                <p className="text-neutral-600 leading-relaxed">{step.description}</p>
                
                {index < steps.length - 1 && (
                  <div className="hidden lg:block absolute top-8 left-0 w-2/3 h-px bg-neutral-200 transform translate-x-1/2" />
                )}
              </div>
            ))}
          </MotionStagger>
        </div>
      </section>

      {/* Features Detail Section */}
      <section className="section-padding bg-neutral-900 text-white overflow-hidden">
        <div className="container-custom">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <MotionSection animation="fade-right">
              <h2 className="text-3xl md:text-4xl font-semibold mb-6">
                Truly Personal, Not Generic
              </h2>
              <p className="text-lg text-neutral-400 mb-8 leading-relaxed">
                Unlike traditional career counseling, Skill Lantern doesn&apos;t rely on vague suggestions or generic aptitude results. Every recommendation is generated based on your actual data.
              </p>
              
              <ul className="space-y-4">
                {[
                  "Academic history and performance analysis",
                  "Personal interests and passion mapping",
                  "Skills assessment and competency evaluation",
                  "Career goal alignment and market fit",
                ].map((item, index) => (
                  <li key={index} className="flex items-center gap-3">
                    <svg className="w-5 h-5 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-neutral-300">{item}</span>
                  </li>
                ))}
              </ul>
            </MotionSection>
            
            <MotionSection animation="fade-left" delay={0.2} className="bg-neutral-800 rounded-2xl p-8 lg:p-12">
              <div className="space-y-6">
                <div className="flex items-center gap-4 hover:translate-x-2 transition-transform">
                  <div className="w-12 h-12 bg-neutral-700 rounded-full flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <div>
                    <div className="font-medium">Profile Analysis</div>
                    <div className="text-sm text-neutral-500">Understanding your unique strengths</div>
                  </div>
                </div>
                
                <div className="h-px bg-neutral-700" />
                
                <div className="flex items-center gap-4 hover:translate-x-2 transition-transform">
                  <div className="w-12 h-12 bg-neutral-700 rounded-full flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <div className="font-medium">AI Processing</div>
                    <div className="text-sm text-neutral-500">Advanced ML algorithms at work</div>
                  </div>
                </div>
                
                <div className="h-px bg-neutral-700" />
                
                <div className="flex items-center gap-4 hover:translate-x-2 transition-transform">
                  <div className="w-12 h-12 bg-neutral-700 rounded-full flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div>
                    <div className="font-medium">Career Match</div>
                    <div className="text-sm text-neutral-500">Personalized recommendations delivered</div>
                  </div>
                </div>
              </div>
            </MotionSection>
          </div>
        </div>
      </section>

      {/* Testimonials/Trust Section */}
      <section className="section-padding">
        <div className="container-custom">
          <MotionSection className="max-w-3xl mx-auto text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-semibold mb-6">
              Built for Students & Professionals
            </h2>
            <p className="text-lg text-neutral-600 leading-relaxed">
              Whether you&apos;re a student exploring career possibilities or a professional planning a career shift, Skill Lantern provides the clarity and direction you need.
            </p>
          </MotionSection>

          <MotionStagger className="grid md:grid-cols-3 gap-8" stagger={0.1}>
            <div className="bg-neutral-50 p-8 rounded-2xl hover-lift">
              <div className="text-4xl mb-4">🎓</div>
              <h3 className="text-lg font-semibold mb-3">For Students</h3>
              <p className="text-neutral-600 leading-relaxed">
                Explore career options early, understand industry requirements, and start building the right skills before graduation.
              </p>
            </div>
            
            <div className="bg-neutral-50 p-8 rounded-2xl hover-lift">
              <div className="text-4xl mb-4">💼</div>
              <h3 className="text-lg font-semibold mb-3">For Job Seekers</h3>
              <p className="text-neutral-600 leading-relaxed">
                Discover careers that match your existing skills, identify gaps, and get actionable steps to land your dream job.
              </p>
            </div>
            
            <div className="bg-neutral-50 p-8 rounded-2xl hover-lift">
              <div className="text-4xl mb-4">🚀</div>
              <h3 className="text-lg font-semibold mb-3">For Professionals</h3>
              <p className="text-neutral-600 leading-relaxed">
                Plan your career transition with confidence. Leverage your experience and learn what&apos;s needed for your next move.
              </p>
            </div>
          </MotionStagger>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-neutral-900 text-white">
        <div className="container-custom text-center">
          <MotionSection animation="scale" className="max-w-3xl mx-auto">
            <h2 className="text-3xl md:text-4xl lg:text-5xl font-semibold mb-6">
              Ready to Discover Your Career Path?
            </h2>
            <p className="text-lg text-neutral-400 mb-10 leading-relaxed">
              Your dream career is closer than you think. Get personalized recommendations, explore detailed roadmaps, and take your first step toward a successful future.
            </p>
            
            <Link
              href="/registration/login"
              className="inline-flex items-center gap-2 bg-white text-neutral-900 px-8 py-4 rounded-lg font-medium hover:bg-neutral-100 transition-all hover:scale-105 btn-press"
            >
              Get Started Free
              <svg className="w-5 h-5 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </Link>
            
            <p className="text-sm text-neutral-500 mt-6">
              No credit card required • Free forever for basic features
            </p>
          </MotionSection>
        </div>
      </section>
    </main>
  );
}
