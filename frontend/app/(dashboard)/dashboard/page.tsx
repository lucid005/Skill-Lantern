"use client";

import { useEffect, useState, Suspense } from "react";
import { useSession, signOut } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import {
  HiOutlineSparkles,
  HiOutlineChartBar,
  HiOutlineAcademicCap,
  HiOutlineArrowRight,
  HiOutlineBuildingOffice2,
  HiOutlineClipboardDocumentList,
  HiOutlineArrowPath,
  HiOutlineUser,
} from "react-icons/hi2";

interface PredictedCareer {
  career: string;
  confidence: number;
  description?: string;
}

interface Recommendation {
  id: string;
  predictions: PredictedCareer[];
  topCareer: string | null;
  hasFullDetails: boolean;
  roadmap?: unknown;
  colleges?: unknown;
  summary?: string;
  immediateActions?: string[];
  createdAt: string;
}

interface UserProfile {
  fullName?: string;
  course?: string;
  specialization?: string;
  interests?: string[];
  technicalSkills?: string[];
  softSkills?: string[];
}

function DashboardContent() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const searchParams = useSearchParams();
  const isNew = searchParams.get("new") === "true";

  const [recommendation, setRecommendation] = useState<Recommendation | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadingFullDetails, setLoadingFullDetails] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showFullDetails, setShowFullDetails] = useState(false);

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/registration/login");
    }
  }, [status, router]);

  useEffect(() => {
    const fetchData = async () => {
      if (status !== "authenticated") return;

      try {
        // Fetch recommendation
        const recResponse = await fetch("/api/users/recommendations");
        if (recResponse.ok) {
          const recData = await recResponse.json();
          setRecommendation(recData);
        }

        // Fetch profile
        const profileResponse = await fetch("/api/users/profile");
        if (profileResponse.ok) {
          const profileData = await profileResponse.json();
          setProfile(profileData);
        }
      } catch (err) {
        console.error("Failed to fetch data:", err);
        setError("Failed to load your recommendations");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [status]);

  const handleGetFullDetails = async () => {
    if (!recommendation || recommendation.hasFullDetails) {
      setShowFullDetails(true);
      return;
    }

    setLoadingFullDetails(true);
    setError(null);

    try {
      const response = await fetch("/api/users/recommendations", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          recommendationId: recommendation.id,
          userProfile: profile,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get full details");
      }

      const updatedRec = await response.json();
      setRecommendation(updatedRec);
      setShowFullDetails(true);
    } catch {
      setError("Failed to load full details. Please try again.");
    } finally {
      setLoadingFullDetails(false);
    }
  };

  const handleSignOut = () => {
    signOut({ callbackUrl: "/" });
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.7) return "text-green-600 bg-green-100";
    if (confidence >= 0.4) return "text-yellow-600 bg-yellow-100";
    return "text-blue-600 bg-blue-100";
  };

  if (status === "loading" || loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-neutral-50 to-neutral-100 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center space-y-4"
        >
          <div className="w-16 h-16 border-4 border-neutral-900 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-neutral-600">Loading your dashboard...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-50 to-neutral-100">
      {/* Header */}
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-8 h-8 bg-neutral-900 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">SL</span>
              </div>
              <span className="text-xl font-semibold tracking-tight">Skill Lantern</span>
            </Link>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-neutral-600">
                <HiOutlineUser size={20} />
                <span className="text-sm">{session?.user?.email}</span>
              </div>
              <button
                onClick={handleSignOut}
                className="px-4 py-2 text-sm text-neutral-600 hover:text-neutral-900 transition-colors"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-neutral-900">
            {isNew ? "🎉 Welcome to Skill Lantern!" : `Welcome back${profile?.fullName ? `, ${profile.fullName}` : ""}!`}
          </h1>
          <p className="text-neutral-600 mt-2">
            {isNew
              ? "Your career recommendations are ready. Here's what our AI found for you."
              : "Here are your personalized career recommendations."}
          </p>
        </motion.div>

        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700"
          >
            {error}
          </motion.div>
        )}

        {!recommendation ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="bg-white rounded-2xl p-8 text-center shadow-sm"
          >
            <HiOutlineSparkles className="w-16 h-16 text-neutral-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold mb-2">No Recommendations Yet</h2>
            <p className="text-neutral-600 mb-6">
              Complete your profile to get personalized career recommendations.
            </p>
            <Link
              href="/registration/signup"
              className="inline-flex items-center gap-2 px-6 py-3 bg-neutral-900 text-white rounded-lg hover:bg-neutral-800 transition-colors"
            >
              Complete Profile
              <HiOutlineArrowRight size={18} />
            </Link>
          </motion.div>
        ) : (
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Career Predictions */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="lg:col-span-2"
            >
              <div className="bg-white rounded-2xl p-6 shadow-sm">
                <div className="flex items-center gap-2 mb-6">
                  <HiOutlineChartBar className="w-6 h-6 text-neutral-900" />
                  <h2 className="text-xl font-semibold">Career Predictions</h2>
                </div>

                <div className="space-y-4">
                  {recommendation.predictions.slice(0, 5).map((prediction, index) => (
                    <motion.div
                      key={prediction.career}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.1 * index }}
                      className={`p-4 rounded-xl border-2 transition-all ${
                        index === 0
                          ? "border-neutral-900 bg-neutral-50"
                          : "border-neutral-200 hover:border-neutral-300"
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            {index === 0 && (
                              <span className="px-2 py-0.5 bg-neutral-900 text-white text-xs rounded-full">
                                Top Match
                              </span>
                            )}
                            <h3 className="font-semibold text-lg">{prediction.career}</h3>
                          </div>
                          {prediction.description && (
                            <p className="text-neutral-600 text-sm mt-1">{prediction.description}</p>
                          )}
                        </div>
                        <span
                          className={`px-3 py-1 rounded-full text-sm font-medium ${getConfidenceColor(
                            prediction.confidence
                          )}`}
                        >
                          {(prediction.confidence * 100).toFixed(1)}%
                        </span>
                      </div>

                      {/* Progress bar */}
                      <div className="mt-3 h-2 bg-neutral-100 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${prediction.confidence * 100}%` }}
                          transition={{ delay: 0.3 + index * 0.1, duration: 0.5 }}
                          className="h-full bg-neutral-900 rounded-full"
                        />
                      </div>
                    </motion.div>
                  ))}
                </div>

                {/* See Full Details Button */}
                <motion.button
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.5 }}
                  onClick={handleGetFullDetails}
                  disabled={loadingFullDetails}
                  className={`mt-6 w-full flex items-center justify-center gap-2 px-6 py-4 bg-neutral-900 text-white rounded-xl hover:bg-neutral-800 transition-all ${
                    loadingFullDetails ? "opacity-70 cursor-not-allowed" : ""
                  }`}
                >
                  {loadingFullDetails ? (
                    <>
                      <HiOutlineArrowPath className="w-5 h-5 animate-spin" />
                      Generating Full Roadmap & College Suggestions...
                    </>
                  ) : (
                    <>
                      <HiOutlineSparkles className="w-5 h-5" />
                      {recommendation.hasFullDetails
                        ? "View Full Career Roadmap & Colleges"
                        : "Get Full Career Roadmap & College Suggestions"}
                      <HiOutlineArrowRight className="w-5 h-5" />
                    </>
                  )}
                </motion.button>
              </div>
            </motion.div>

            {/* Profile Summary */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <div className="bg-white rounded-2xl p-6 shadow-sm">
                <div className="flex items-center gap-2 mb-6">
                  <HiOutlineUser className="w-6 h-6 text-neutral-900" />
                  <h2 className="text-xl font-semibold">Your Profile</h2>
                </div>

                {profile && (
                  <div className="space-y-4 text-sm">
                    {profile.course && (
                      <div>
                        <span className="text-neutral-500">Course</span>
                        <p className="font-medium">{profile.course}</p>
                      </div>
                    )}
                    {profile.specialization && (
                      <div>
                        <span className="text-neutral-500">Specialization</span>
                        <p className="font-medium">{profile.specialization}</p>
                      </div>
                    )}
                    {profile.interests && profile.interests.length > 0 && (
                      <div>
                        <span className="text-neutral-500">Interests</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {profile.interests.map((interest) => (
                            <span
                              key={interest}
                              className="px-2 py-1 bg-neutral-100 rounded text-xs"
                            >
                              {interest}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                    {(profile.technicalSkills?.length || profile.softSkills?.length) && (
                      <div>
                        <span className="text-neutral-500">Skills</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {[...(profile.technicalSkills || []), ...(profile.softSkills || [])].map((skill) => (
                            <span
                              key={skill}
                              className="px-2 py-1 bg-blue-50 text-blue-700 rounded text-xs"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Quick Stats */}
              <div className="bg-white rounded-2xl p-6 shadow-sm mt-6">
                <h3 className="font-semibold mb-4">Quick Stats</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-3 bg-neutral-50 rounded-xl">
                    <p className="text-2xl font-bold text-neutral-900">
                      {recommendation.predictions.length}
                    </p>
                    <p className="text-xs text-neutral-500">Careers Matched</p>
                  </div>
                  <div className="text-center p-3 bg-neutral-50 rounded-xl">
                    <p className="text-2xl font-bold text-neutral-900">
                      {((recommendation.predictions[0]?.confidence || 0) * 100).toFixed(0)}%
                    </p>
                    <p className="text-xs text-neutral-500">Top Match Score</p>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        )}

        {/* Full Details Modal */}
        <AnimatePresence>
          {showFullDetails && recommendation?.hasFullDetails && (
            <FullDetailsModal
              recommendation={recommendation}
              onClose={() => setShowFullDetails(false)}
            />
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

// Full Details Modal Component
function FullDetailsModal({
  recommendation,
  onClose,
}: {
  recommendation: Recommendation;
  onClose: () => void;
}) {
  const roadmap = recommendation.roadmap as {
    career?: string;
    overview?: string;
    stages?: Array<{
      level: string;
      duration: string;
      skills: string[];
      resources: string[];
      milestones: string[];
    }>;
    tools_and_technologies?: string[];
    job_roles?: string[];
    growth_paths?: string[];
  } | null;

  const colleges = recommendation.colleges as {
    recommendations?: Array<{
      name: string;
      location: string;
      programs?: string[];
      reason?: string;
    }>;
    alternatives?: Array<{
      name: string;
      location: string;
    }>;
  } | null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 z-50 flex items-start justify-center overflow-y-auto py-8"
      onClick={onClose}
    >
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 50 }}
        className="bg-white rounded-2xl max-w-4xl w-full mx-4 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-neutral-900 text-white p-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold">Career Roadmap</h2>
              <p className="text-neutral-300">{roadmap?.career || recommendation.topCareer}</p>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-white/10 rounded-lg transition-colors"
            >
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <div className="p-6 space-y-8 max-h-[70vh] overflow-y-auto">
          {/* Summary */}
          {recommendation.summary && (
            <section>
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <HiOutlineSparkles className="w-5 h-5" />
                Summary
              </h3>
              <p className="text-neutral-600 leading-relaxed">{recommendation.summary}</p>
            </section>
          )}

          {/* Immediate Actions */}
          {recommendation.immediateActions && recommendation.immediateActions.length > 0 && (
            <section>
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <HiOutlineClipboardDocumentList className="w-5 h-5" />
                Immediate Actions
              </h3>
              <ul className="space-y-2">
                {recommendation.immediateActions.map((action, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <span className="w-6 h-6 rounded-full bg-neutral-900 text-white text-xs flex items-center justify-center shrink-0 mt-0.5">
                      {index + 1}
                    </span>
                    <span className="text-neutral-600">{action}</span>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Career Stages */}
          {roadmap?.stages && roadmap.stages.length > 0 && (
            <section>
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <HiOutlineChartBar className="w-5 h-5" />
                Career Roadmap Stages
              </h3>
              <div className="space-y-4">
                {roadmap.stages.map((stage, index) => (
                  <div
                    key={index}
                    className="border-2 border-neutral-200 rounded-xl p-4 hover:border-neutral-300 transition-colors"
                  >
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="font-semibold">{stage.level}</h4>
                      <span className="text-sm text-neutral-500">{stage.duration}</span>
                    </div>
                    {stage.skills.length > 0 && (
                      <div className="mb-2">
                        <span className="text-xs text-neutral-500">Skills to Learn:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {stage.skills.map((skill) => (
                            <span key={skill} className="px-2 py-1 bg-blue-50 text-blue-700 rounded text-xs">
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                    {stage.milestones.length > 0 && (
                      <div>
                        <span className="text-xs text-neutral-500">Milestones:</span>
                        <ul className="mt-1 text-sm text-neutral-600">
                          {stage.milestones.map((milestone, i) => (
                            <li key={i} className="flex items-start gap-1">
                              <span className="text-green-500">✓</span>
                              {milestone}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Colleges */}
          {colleges?.recommendations && colleges.recommendations.length > 0 && (
            <section>
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <HiOutlineAcademicCap className="w-5 h-5" />
                Recommended Colleges in Nepal
              </h3>
              <div className="grid md:grid-cols-2 gap-4">
                {colleges.recommendations.map((college, index) => (
                  <div
                    key={index}
                    className="border border-neutral-200 rounded-xl p-4 hover:border-neutral-300 transition-colors"
                  >
                    <h4 className="font-semibold">{college.name}</h4>
                    <p className="text-sm text-neutral-500 flex items-center gap-1 mt-1">
                      <HiOutlineBuildingOffice2 className="w-4 h-4" />
                      {college.location}
                    </p>
                    {college.programs && college.programs.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-2">
                        {college.programs.slice(0, 3).map((program) => (
                          <span key={program} className="px-2 py-0.5 bg-neutral-100 text-xs rounded">
                            {program}
                          </span>
                        ))}
                      </div>
                    )}
                    {college.reason && (
                      <p className="text-xs text-neutral-500 mt-2">{college.reason}</p>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Tools & Technologies */}
          {roadmap?.tools_and_technologies && roadmap.tools_and_technologies.length > 0 && (
            <section>
              <h3 className="text-lg font-semibold mb-3">Tools & Technologies</h3>
              <div className="flex flex-wrap gap-2">
                {roadmap.tools_and_technologies.map((tool) => (
                  <span key={tool} className="px-3 py-1.5 bg-neutral-100 rounded-lg text-sm">
                    {tool}
                  </span>
                ))}
              </div>
            </section>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-neutral-200 p-4 flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-neutral-900 text-white rounded-lg hover:bg-neutral-800 transition-colors"
          >
            Close
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}

export default function DashboardPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-br from-neutral-50 to-neutral-100 flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-neutral-900 border-t-transparent rounded-full animate-spin"></div>
      </div>
    }>
      <DashboardContent />
    </Suspense>
  );
}
