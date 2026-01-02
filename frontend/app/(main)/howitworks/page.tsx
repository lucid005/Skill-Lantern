"use client";

import Link from "next/link";
import { GSAPSection, GSAPStagger } from "@/components/GSAPAnimations";

export default function HowItWorks() {
  const steps = [
    {
      number: "01",
      title: "Create Your Profile",
      description: "Sign up and tell us about yourself. We'll ask about your educational background, skills, interests, and career aspirations to build a comprehensive profile.",
      details: [
        "Academic history and qualifications",
        "Technical and soft skills assessment",
        "Personal interests and hobbies",
        "Career goals and preferences",
      ],
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      ),
    },
    {
      number: "02",
      title: "Complete the Assessment",
      description: "Take our comprehensive career assessment designed to understand your strengths, preferences, and potential. This typically takes 15-20 minutes to complete.",
      details: [
        "Aptitude and ability tests",
        "Personality trait evaluation",
        "Work style preferences",
        "Value and motivation mapping",
      ],
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
      ),
    },
    {
      number: "03",
      title: "AI Analysis",
      description: "Our advanced XGBoost machine learning model analyzes your profile against thousands of career paths, considering industry requirements, job market trends, and success patterns.",
      details: [
        "Multi-dimensional profile analysis",
        "10,000+ career path matching",
        "Market demand consideration",
        "Success pattern recognition",
      ],
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      ),
    },
    {
      number: "04",
      title: "Get Your Recommendations",
      description: "Receive personalized career recommendations with detailed insights. Each recommendation includes a match score, required skills, potential salary, and growth outlook.",
      details: [
        "Top career matches with scores",
        "Detailed career descriptions",
        "Salary and growth projections",
        "Required skills breakdown",
      ],
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
    {
      number: "05",
      title: "Explore Your Roadmap",
      description: "Access your personalized learning roadmap with step-by-step guidance. Get curated courses, certifications, and resources to help you achieve your career goals.",
      details: [
        "Structured learning paths",
        "Course and certification links",
        "Milestone tracking",
        "Resource recommendations",
      ],
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
        </svg>
      ),
    },
    {
      number: "06",
      title: "Track Your Progress",
      description: "Monitor your career development journey with our progress dashboard. Update your skills, track completed courses, and see how your career readiness improves over time.",
      details: [
        "Visual progress tracking",
        "Skill development metrics",
        "Achievement badges",
        "Periodic reassessments",
      ],
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
      ),
    },
  ];

  const faqs = [
    {
      question: "How long does the assessment take?",
      answer: "The comprehensive career assessment typically takes 15-20 minutes to complete. We recommend doing it in one sitting for the most accurate results.",
    },
    {
      question: "How accurate are the recommendations?",
      answer: "Our AI model has a 95% accuracy rate in matching users with suitable careers. The recommendations are based on extensive data analysis and continuous learning from user outcomes.",
    },
    {
      question: "Can I retake the assessment?",
      answer: "Yes! You can retake the assessment anytime. We recommend updating your profile every 6-12 months or after significant changes in your skills or goals.",
    },
    {
      question: "Is my data secure?",
      answer: "Absolutely. We use industry-standard encryption and never share your personal information with third parties. Your data is used solely to provide personalized recommendations.",
    },
  ];

  return (
    <main className="flex flex-col pt-20">
      {/* Hero Section */}
      <section className="section-padding">
        <div className="container-custom text-center">
          <GSAPSection className="max-w-3xl mx-auto">
            <div className="badge mb-6">Simple Process</div>
            <h1 className="text-4xl md:text-5xl font-semibold mb-6">
              How Skill Lantern
              <br />
              <span className="gradient-text">Works for You</span>
            </h1>
            <p className="text-lg text-neutral-600 leading-relaxed">
              From profile creation to career success—discover our simple, effective process that guides you every step of the way.
            </p>
          </GSAPSection>
        </div>
      </section>

      {/* Steps Section */}
      <section className="section-padding bg-neutral-50">
        <div className="container-custom">
          <div className="max-w-4xl mx-auto">
            {steps.map((step, index) => (
              <GSAPSection
                key={index}
                animation="fade-up"
                delay={index * 0.05}
                className="relative pl-8 md:pl-16 pb-16 last:pb-0"
              >
                {/* Timeline Line */}
                {index !== steps.length - 1 && (
                  <div className="absolute left-0 md:left-6 top-16 w-px h-full bg-neutral-300" />
                )}

                {/* Step Number */}
                <div className="absolute left-0 md:left-0 top-0 w-12 h-12 bg-neutral-900 text-white rounded-full flex items-center justify-center font-semibold text-sm">
                  {step.number}
                </div>

                {/* Content */}
                <div className="bg-white rounded-2xl p-8 border border-neutral-200 ml-8 md:ml-12">
                  <div className="flex items-start gap-4 mb-4">
                    <div className="w-12 h-12 bg-neutral-100 rounded-xl flex items-center justify-center text-neutral-700 shrink-0">
                      {step.icon}
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
                      <p className="text-neutral-600 leading-relaxed">
                        {step.description}
                      </p>
                    </div>
                  </div>

                  <div className="ml-16 mt-6">
                    <ul className="grid md:grid-cols-2 gap-3">
                      {step.details.map((detail, idx) => (
                        <li key={idx} className="flex items-center gap-2">
                          <svg
                            className="w-4 h-4 text-neutral-500"
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
                          <span className="text-sm text-neutral-600">{detail}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </GSAPSection>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="section-padding">
        <div className="container-custom">
          <div className="max-w-3xl mx-auto">
            <GSAPSection className="text-center mb-12">
              <h2 className="text-3xl font-semibold mb-4">
                Frequently Asked Questions
              </h2>
              <p className="text-neutral-600">
                Got questions? We&apos;ve got answers.
              </p>
            </GSAPSection>

            <GSAPStagger className="space-y-4" stagger={0.08}>
              {faqs.map((faq, index) => (
                <div
                  key={index}
                  className="bg-neutral-50 rounded-xl p-6"
                >
                  <h3 className="font-semibold mb-2">{faq.question}</h3>
                  <p className="text-neutral-600">{faq.answer}</p>
                </div>
              ))}
            </GSAPStagger>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-neutral-900 text-white">
        <div className="container-custom text-center">
          <GSAPSection animation="scale" className="max-w-2xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-semibold mb-6">
              Ready to Start Your Journey?
            </h2>
            <p className="text-neutral-400 mb-8">
              Join thousands of users who have discovered their ideal career path with Skill Lantern.
            </p>
            <Link
              href="/registration/login"
              className="inline-flex items-center gap-2 bg-white text-neutral-900 px-8 py-4 rounded-lg font-medium hover:bg-neutral-100 transition-colors"
            >
              Start Free Assessment
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
          </GSAPSection>
        </div>
      </section>
    </main>
  );
}
