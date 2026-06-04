"use client";

import { useEffect, useMemo, useState, Suspense } from "react";
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
  HiOutlineMap,
  HiOutlineBookOpen,
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
  roadmapProgress?: Record<string, boolean> | null;
  userFeedback?: "helpful" | "not_helpful" | null;
  feedbackComment?: string | null;
  feedbackCreatedAt?: string | null;
  createdAt: string;
}

interface UserProfile {
  fullName?: string;
  course?: string;
  specialization?: string;
  interests?: string[];
  technicalSkills?: string[];
  softSkills?: string[];
  cgpa?: number | null;
  cityRegion?: string | null;
  careerLifestyle?: string | null;
  workEnvironment?: string | null;
  locationPreference?: string | null;
  learningStyle?: string | null;
}

function DashboardContent() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const searchParams = useSearchParams();
  const isNew = searchParams.get("new") === "true";

  const [recommendation, setRecommendation] = useState<Recommendation | null>(null);
  const [recommendationHistory, setRecommendationHistory] = useState<Recommendation[]>([]);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadingFullDetails, setLoadingFullDetails] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generatingRecs, setGeneratingRecs] = useState(false);
  const [profileSaving, setProfileSaving] = useState(false);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/registration/login");
    }
  }, [status, router]);

  useEffect(() => {
    const fetchData = async () => {
      if (status !== "authenticated") return;

      try {
        // Fetch recommendations
        const recResponse = await fetch("/api/users/recommendations?all=true");
        if (recResponse.ok) {
          const recData = await recResponse.json();
          const recs = Array.isArray(recData) ? recData : [];
          setRecommendationHistory(recs);
          setRecommendation(recs[0] || null);
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
      setRecommendationHistory((items) =>
        items.map((item) => (item.id === updatedRec.id ? updatedRec : item))
      );
    } catch {
      setError("Failed to load full details. Please try again.");
    } finally {
      setLoadingFullDetails(false);
    }
  };

  const handleRetryRecommendations = async () => {
    setGeneratingRecs(true);
    setError(null);

    try {
      const response = await fetch("/api/users/recommendations", {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Failed to generate recommendations");
      }

      const data = await response.json();
      setRecommendation(data);
      setRecommendationHistory((items) => [data, ...items]);
    } catch {
      setError("Failed to generate recommendations. Make sure the AI backend is running.");
    } finally {
      setGeneratingRecs(false);
    }
  };

  const handleSignOut = () => {
    signOut({ callbackUrl: "/" });
  };

  const handleProfileSave = async (nextProfile: UserProfile) => {
    setProfileSaving(true);
    setError(null);

    try {
      const response = await fetch("/api/users/profile", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(nextProfile),
      });

      if (!response.ok) {
        throw new Error("Failed to update profile");
      }

      const updatedProfile = await response.json();
      setProfile(updatedProfile);
    } catch {
      setError("Failed to update profile. Please try again.");
    } finally {
      setProfileSaving(false);
    }
  };

  const updateRecommendation = (updated: Recommendation) => {
    setRecommendation(updated);
    setRecommendationHistory((items) =>
      items.map((item) => (item.id === updated.id ? updated : item))
    );
  };

  const handleFeedback = async (
    userFeedback: "helpful" | "not_helpful",
    feedbackComment: string
  ) => {
    if (!recommendation) return;

    try {
      const response = await fetch("/api/users/recommendations", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "feedback",
          recommendationId: recommendation.id,
          userFeedback,
          feedbackComment,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to save feedback");
      }

      updateRecommendation(await response.json());
    } catch {
      setError("Failed to save feedback. Please try again.");
    }
  };

  const handleRoadmapProgress = async (roadmapProgress: Record<string, boolean>) => {
    if (!recommendation) return;

    const optimistic = { ...recommendation, roadmapProgress };
    updateRecommendation(optimistic);

    try {
      const response = await fetch("/api/users/recommendations", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "roadmap_progress",
          recommendationId: recommendation.id,
          roadmapProgress,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to save progress");
      }

      updateRecommendation(await response.json());
    } catch {
      setError("Progress was updated locally but could not be saved.");
    }
  };



  if (status === "loading" || loading) {
    return (
      <div className="min-h-screen bg-linear-to-br from-neutral-50 to-neutral-100 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center space-y-6"
        >
          <div className="relative">
            <div className="w-20 h-20 border-4 border-neutral-200 border-t-neutral-900 rounded-full animate-spin mx-auto"></div>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: [0, 1.2, 1] }}
              transition={{ delay: 0.3, duration: 0.5 }}
              className="absolute inset-0 flex items-center justify-center"
            >
              <div className="w-8 h-8 bg-neutral-900 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xs">SL</span>
              </div>
            </motion.div>
          </div>
          <div className="space-y-2">
            <p className="text-neutral-900 font-semibold text-lg">Loading your dashboard</p>
            <p className="text-neutral-500 text-sm">Preparing your personalized insights...</p>
          </div>
          <div className="flex items-center gap-1.5 justify-center">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="w-2 h-2 bg-neutral-400 rounded-full"
                animate={{ opacity: [0.3, 1, 0.3] }}
                transition={{ duration: 1.2, repeat: Infinity, delay: i * 0.2 }}
              />
            ))}
          </div>
        </motion.div>
      </div>
    );
  }

  const tabs = [
    { id: "overview", label: "Overview", icon: HiOutlineChartBar },
    { id: "roadmap", label: "Career Roadmap", icon: HiOutlineMap },
    { id: "colleges", label: "College Recommendations", icon: HiOutlineAcademicCap },
    { id: "summary", label: "Full Summary", icon: HiOutlineBookOpen },
  ];

  return (
    <div className="min-h-screen bg-linear-to-br from-neutral-50 to-neutral-100">
      {/* Header */}
      <header className="bg-white border-b border-neutral-200 sticky top-0 z-40">
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
          <h1 className="text-4xl font-bold text-neutral-900">
            {isNew ? "🎉 Welcome to Skill Lantern!" : `Welcome back${profile?.fullName ? `, ${profile.fullName}` : ""}!`}
          </h1>
          <p className="text-neutral-600 mt-2 text-lg">
            Discover your perfect career path with AI-powered recommendations
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
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl p-12 text-center shadow-sm border border-neutral-100"
          >
            {generatingRecs ? (
              <div className="space-y-6">
                <div className="relative">
                  <div className="w-16 h-16 border-4 border-neutral-200 border-t-neutral-900 rounded-full animate-spin mx-auto"></div>
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: [0, 1.2, 1] }}
                    transition={{ delay: 0.3, duration: 0.5 }}
                    className="absolute inset-0 flex items-center justify-center"
                  >
                    <HiOutlineSparkles className="w-6 h-6 text-neutral-700" />
                  </motion.div>
                </div>
                <div>
                  <h2 className="text-xl font-semibold mb-2">Generating Your Recommendations</h2>
                  <p className="text-neutral-500 text-sm">Our AI is analyzing your profile. This may take a moment...</p>
                </div>
                <div className="flex items-center gap-1.5 justify-center">
                  {[0, 1, 2].map((i) => (
                    <motion.div
                      key={i}
                      className="w-2 h-2 bg-neutral-400 rounded-full"
                      animate={{ opacity: [0.3, 1, 0.3] }}
                      transition={{ duration: 1.2, repeat: Infinity, delay: i * 0.2 }}
                    />
                  ))}
                </div>
              </div>
            ) : (
              <>
                <div className="w-20 h-20 bg-neutral-50 rounded-2xl flex items-center justify-center mx-auto mb-6 border border-neutral-100">
                  <HiOutlineSparkles className="w-10 h-10 text-neutral-400" />
                </div>
                <h2 className="text-2xl font-bold mb-3">No Recommendations Yet</h2>
                <p className="text-neutral-500 mb-8 max-w-md mx-auto">
                  {error
                    ? "We couldn't generate your recommendations. The AI backend may be offline."
                    : "Complete your profile to get personalized career recommendations."}
                </p>
                <div className="flex items-center gap-3 justify-center">
                  <button
                    onClick={handleRetryRecommendations}
                    className="inline-flex items-center gap-2 px-6 py-3 bg-neutral-900 text-white rounded-xl hover:bg-neutral-800 transition-colors font-medium"
                  >
                    <HiOutlineSparkles size={18} />
                    Generate Recommendations
                  </button>
                  <Link
                    href="/registration/signup"
                    className="inline-flex items-center gap-2 px-6 py-3 border-2 border-neutral-200 text-neutral-700 rounded-xl hover:border-neutral-300 transition-colors font-medium"
                  >
                    Update Profile
                    <HiOutlineArrowRight size={18} />
                  </Link>
                </div>
              </>
            )}
          </motion.div>
        ) : (
          <div className="space-y-6">
            {recommendationHistory.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-2xl p-5 shadow-sm border border-neutral-100"
              >
                <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                  <div>
                    <h2 className="font-bold text-neutral-900">Recommendation History</h2>
                    <p className="text-sm text-neutral-500">
                      Compare previous AI runs or print the selected recommendation.
                    </p>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <button
                      onClick={handleRetryRecommendations}
                      disabled={generatingRecs}
                      className="px-4 py-2 rounded-lg text-sm font-medium bg-neutral-900 text-white disabled:opacity-60"
                    >
                      {generatingRecs ? "Generating..." : "Generate New"}
                    </button>
                    {recommendationHistory.slice(0, 5).map((item) => (
                      <button
                        key={item.id}
                        onClick={() => setRecommendation(item)}
                        className={`px-4 py-2 rounded-lg text-sm font-medium border transition-colors ${
                          item.id === recommendation.id
                            ? "bg-neutral-900 text-white border-neutral-900"
                            : "bg-white text-neutral-700 border-neutral-200 hover:border-neutral-400"
                        }`}
                      >
                        {item.topCareer || "Recommendation"} · {new Date(item.createdAt).toLocaleDateString()}
                      </button>
                    ))}
                    <button
                      onClick={() => window.print()}
                      className="px-4 py-2 rounded-lg text-sm font-medium border border-neutral-200 text-neutral-700 hover:border-neutral-400"
                    >
                      Print / Save PDF
                    </button>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Tab Navigation */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="flex gap-2 border-b border-neutral-200 bg-white rounded-t-2xl p-4 overflow-x-auto"
            >
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-2 px-4 py-3 rounded-lg font-medium transition-all whitespace-nowrap ${
                      activeTab === tab.id
                        ? "bg-neutral-900 text-white"
                        : "text-neutral-600 hover:text-neutral-900 bg-neutral-50 hover:bg-neutral-100"
                    }`}
                  >
                    <Icon size={18} />
                    {tab.label}
                  </button>
                );
              })}
            </motion.div>

            {/* Tab Content */}
            <AnimatePresence mode="wait">
              {activeTab === "overview" && (
                <motion.div
                  key="overview"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-6"
                >
                  <OverviewTab
                    recommendation={recommendation}
                    profile={profile}
                    onProfileSave={handleProfileSave}
                    profileSaving={profileSaving}
                  />
                </motion.div>
              )}

              {activeTab === "roadmap" && (
                <motion.div
                  key="roadmap"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-6"
                >
                  <RoadmapTab
                    recommendation={recommendation}
                    loadingFullDetails={loadingFullDetails}
                    onGetFullDetails={handleGetFullDetails}
                    onProgressChange={handleRoadmapProgress}
                  />
                </motion.div>
              )}

              {activeTab === "colleges" && (
                <motion.div
                  key="colleges"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-6"
                >
                  <CollegesTab recommendation={recommendation} />
                </motion.div>
              )}

              {activeTab === "summary" && (
                <motion.div
                  key="summary"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-6"
                >
                  <SummaryTab
                    key={recommendation.id}
                    recommendation={recommendation}
                    onFeedback={handleFeedback}
                  />
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}
      </main>
    </div>
  );
}

// Overview Tab Component
function OverviewTab({
  recommendation,
  profile,
  onProfileSave,
  profileSaving,
}: {
  recommendation: Recommendation;
  profile: UserProfile | null;
  onProfileSave: (profile: UserProfile) => Promise<void>;
  profileSaving: boolean;
}) {
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [profileDraft, setProfileDraft] = useState<UserProfile>(profile || {});

  const updateDraft = (field: keyof UserProfile, value: string | string[]) => {
    setProfileDraft((current) => ({ ...current, [field]: value }));
  };

  const splitList = (value?: string[] | null) => (value || []).join(", ");
  const parseList = (value: string) =>
    value
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.7) return "text-green-600 bg-green-100 border-green-200";
    if (confidence >= 0.4) return "text-yellow-600 bg-yellow-100 border-yellow-200";
    return "text-blue-600 bg-blue-100 border-blue-200";
  };

  return (
    <div className="grid lg:grid-cols-3 gap-6">
      {/* Career Predictions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="lg:col-span-2"
      >
        <div className="bg-white rounded-2xl p-8 shadow-sm border border-neutral-100">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-neutral-900 rounded-xl flex items-center justify-center">
                <HiOutlineChartBar className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold">Career Predictions</h2>
                <p className="text-neutral-500 text-sm">Based on your profile analysis</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            {recommendation.predictions.slice(0, 5).map((prediction, index) => (
              <motion.div
                key={prediction.career}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
                className={`p-6 rounded-xl border-2 transition-all ${
                  index === 0
                    ? "border-neutral-900 bg-linear-to-br from-neutral-50 to-neutral-100 shadow-md"
                    : "border-neutral-100 hover:border-neutral-300 bg-white hover:shadow-md"
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      {index === 0 && (
                        <span className="px-3 py-1 bg-neutral-900 text-white text-xs rounded-full font-semibold">
                          🏆 Top Match
                        </span>
                      )}
                      {index === 1 && (
                        <span className="px-3 py-1 bg-blue-100 text-blue-700 text-xs rounded-full font-semibold">
                          🎯 Strong Match
                        </span>
                      )}
                    </div>
                    <h3 className="font-bold text-xl">{prediction.career}</h3>
                  </div>
                  <span
                    className={`px-4 py-2 rounded-full text-sm font-bold border-2 ${getConfidenceColor(
                      prediction.confidence
                    )}`}
                  >
                    {(prediction.confidence * 100).toFixed(1)}%
                  </span>
                </div>

                {prediction.description && (
                  <p className="text-neutral-700 text-sm mb-4 leading-relaxed">
                    {prediction.description}
                  </p>
                )}

                {/* Progress bar */}
                <div className="h-3 bg-neutral-200 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${prediction.confidence * 100}%` }}
                    transition={{ delay: 0.3 + index * 0.1, duration: 0.8 }}
                    className={`h-full rounded-full ${
                      index === 0
                        ? "bg-neutral-900"
                        : index === 1
                        ? "bg-blue-500"
                        : "bg-neutral-600"
                    }`}
                  />
                </div>
              </motion.div>
            ))}
          </div>
          <div className="mt-6 rounded-xl border border-blue-200 bg-blue-50 p-4 text-sm text-blue-900">
            Treat these as a ranked shortlist, not a fixed answer. The model is strongest when you compare the top few matches and read the fit explanation for each one.
          </div>
        </div>
      </motion.div>

      {/* Profile & Quick Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="space-y-6"
      >
        {/* Profile Summary */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-neutral-100">
          <div className="flex items-center justify-between gap-3 mb-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-neutral-900 rounded-xl flex items-center justify-center">
                <HiOutlineUser className="w-5 h-5 text-white" />
              </div>
              <h2 className="text-xl font-bold">Your Profile</h2>
            </div>
            <button
              onClick={() => {
                setProfileDraft(profile || {});
                setIsEditingProfile((value) => !value);
              }}
              className="text-sm font-medium text-neutral-600 hover:text-neutral-900"
            >
              {isEditingProfile ? "Cancel" : "Edit"}
            </button>
          </div>

          {isEditingProfile ? (
            <div className="space-y-4 text-sm">
              <label className="block">
                <span className="text-neutral-500 text-xs font-semibold">Full Name</span>
                <input
                  value={profileDraft.fullName || ""}
                  onChange={(event) => updateDraft("fullName", event.target.value)}
                  className="mt-1 w-full rounded-lg border border-neutral-200 px-3 py-2 outline-none focus:border-neutral-900"
                />
              </label>
              <label className="block">
                <span className="text-neutral-500 text-xs font-semibold">Course</span>
                <input
                  value={profileDraft.course || ""}
                  onChange={(event) => updateDraft("course", event.target.value)}
                  className="mt-1 w-full rounded-lg border border-neutral-200 px-3 py-2 outline-none focus:border-neutral-900"
                />
              </label>
              <label className="block">
                <span className="text-neutral-500 text-xs font-semibold">Specialization</span>
                <input
                  value={profileDraft.specialization || ""}
                  onChange={(event) => updateDraft("specialization", event.target.value)}
                  className="mt-1 w-full rounded-lg border border-neutral-200 px-3 py-2 outline-none focus:border-neutral-900"
                />
              </label>
              <label className="block">
                <span className="text-neutral-500 text-xs font-semibold">City / Region</span>
                <input
                  value={profileDraft.cityRegion || ""}
                  onChange={(event) => updateDraft("cityRegion", event.target.value)}
                  className="mt-1 w-full rounded-lg border border-neutral-200 px-3 py-2 outline-none focus:border-neutral-900"
                />
              </label>
              <label className="block">
                <span className="text-neutral-500 text-xs font-semibold">Technical Skills</span>
                <input
                  value={splitList(profileDraft.technicalSkills)}
                  onChange={(event) => updateDraft("technicalSkills", parseList(event.target.value))}
                  className="mt-1 w-full rounded-lg border border-neutral-200 px-3 py-2 outline-none focus:border-neutral-900"
                />
              </label>
              <label className="block">
                <span className="text-neutral-500 text-xs font-semibold">Soft Skills</span>
                <input
                  value={splitList(profileDraft.softSkills)}
                  onChange={(event) => updateDraft("softSkills", parseList(event.target.value))}
                  className="mt-1 w-full rounded-lg border border-neutral-200 px-3 py-2 outline-none focus:border-neutral-900"
                />
              </label>
              <button
                onClick={async () => {
                  await onProfileSave(profileDraft);
                  setIsEditingProfile(false);
                }}
                disabled={profileSaving}
                className="w-full rounded-lg bg-neutral-900 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-60"
              >
                {profileSaving ? "Saving..." : "Save Profile"}
              </button>
            </div>
          ) : profile ? (
            <div className="space-y-4 text-sm">
              {profile.fullName && (
                <div className="pb-3 border-b border-neutral-100">
                  <span className="text-neutral-500 text-xs font-semibold">Full Name</span>
                  <p className="font-bold text-base mt-1">{profile.fullName}</p>
                </div>
              )}
              {profile.course && (
                <div className="pb-3 border-b border-neutral-100">
                  <span className="text-neutral-500 text-xs font-semibold">Course</span>
                  <p className="font-medium mt-1">{profile.course}</p>
                </div>
              )}
              {profile.specialization && (
                <div className="pb-3 border-b border-neutral-100">
                  <span className="text-neutral-500 text-xs font-semibold">Specialization</span>
                  <p className="font-medium mt-1">{profile.specialization}</p>
                </div>
              )}
              {profile.interests && profile.interests.length > 0 && (
                <div>
                  <span className="text-neutral-500 text-xs font-semibold">Interests</span>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {profile.interests.map((interest) => (
                      <span
                        key={interest}
                        className="px-3 py-1.5 bg-blue-50 text-blue-700 rounded-lg text-xs font-medium"
                      >
                        {interest}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              {profile.technicalSkills && profile.technicalSkills.length > 0 && (
                <div>
                  <span className="text-neutral-500 text-xs font-semibold">Skills</span>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {profile.technicalSkills.slice(0, 8).map((skill) => (
                      <span
                        key={skill}
                        className="px-3 py-1.5 bg-neutral-100 text-neutral-700 rounded-lg text-xs font-medium"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <p className="text-sm text-neutral-500">No profile data found.</p>
          )}
        </div>

        {/* Quick Stats */}
        <div className="bg-linear-to-br from-neutral-900 to-neutral-800 rounded-2xl p-6 shadow-md text-white">
          <h3 className="font-bold mb-4 text-neutral-200 text-sm">Quick Stats</h3>
          <div className="space-y-3">
            <div className="p-4 bg-white/10 rounded-xl backdrop-blur-sm border border-white/20">
              <p className="text-3xl font-bold">
                {recommendation.predictions.length}
              </p>
              <p className="text-xs text-neutral-300 mt-1">Careers Matched</p>
            </div>
            <div className="p-4 bg-white/10 rounded-xl backdrop-blur-sm border border-white/20">
              <p className="text-3xl font-bold">
                {((recommendation.predictions[0]?.confidence || 0) * 100).toFixed(0)}%
              </p>
              <p className="text-xs text-neutral-300 mt-1">Top Match Score</p>
            </div>
            <div className="p-4 bg-white/10 rounded-xl backdrop-blur-sm border border-white/20">
              <p className="text-lg font-bold">
                {recommendation.topCareer}
              </p>
              <p className="text-xs text-neutral-300 mt-1">Recommended Career</p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

// Roadmap Tab Component
function RoadmapTab({
  recommendation,
  loadingFullDetails,
  onGetFullDetails,
  onProgressChange,
}: {
  recommendation: Recommendation;
  loadingFullDetails: boolean;
  onGetFullDetails: () => void;
  onProgressChange: (roadmapProgress: Record<string, boolean>) => Promise<void>;
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
  const progress = recommendation.roadmapProgress || {};
  const milestoneKeys = useMemo(() => {
    return (roadmap?.stages || []).flatMap((stage, stageIndex) =>
      (stage.milestones || []).map((_, milestoneIndex) => `${stageIndex}-${milestoneIndex}`)
    );
  }, [roadmap?.stages]);
  const completedCount = milestoneKeys.filter((key) => progress[key]).length;
  const completionPercent = milestoneKeys.length > 0
    ? Math.round((completedCount / milestoneKeys.length) * 100)
    : 0;

  const toggleMilestone = (key: string) => {
    onProgressChange({
      ...progress,
      [key]: !progress[key],
    });
  };

  if (!recommendation.hasFullDetails) {
    return (
      <div className="bg-white rounded-2xl p-12 text-center shadow-sm border border-neutral-100">
        <div className="w-20 h-20 bg-neutral-50 rounded-2xl flex items-center justify-center mx-auto mb-6 border border-neutral-100">
          <HiOutlineMap className="w-10 h-10 text-neutral-400" />
        </div>
        <h2 className="text-2xl font-bold mb-3">Career Roadmap Details</h2>
        <p className="text-neutral-500 mb-8 max-w-lg mx-auto leading-relaxed">
          Get a comprehensive career roadmap with detailed stages, required skills, milestones, job roles, and growth paths to help you plan your career effectively.
        </p>
        <motion.button
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          onClick={onGetFullDetails}
          disabled={loadingFullDetails}
          className={`inline-flex items-center justify-center gap-2 px-8 py-4 bg-neutral-900 text-white rounded-xl hover:bg-neutral-800 transition-all font-semibold ${
            loadingFullDetails ? "opacity-70 cursor-not-allowed" : ""
          }`}
        >
          {loadingFullDetails ? (
            <>
              <HiOutlineArrowPath className="w-5 h-5 animate-spin" />
              Generating Roadmap...
            </>
          ) : (
            <>
              <HiOutlineSparkles className="w-5 h-5" />
              Generate Full Career Roadmap
              <HiOutlineArrowRight className="w-5 h-5" />
            </>

              
          )}
        </motion.button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {milestoneKeys.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-6 shadow-sm border border-neutral-100"
        >
          <div className="flex items-center justify-between mb-3">
            <div>
              <h3 className="font-bold text-neutral-900">Roadmap Progress</h3>
              <p className="text-sm text-neutral-500">
                {completedCount} of {milestoneKeys.length} milestones completed
              </p>
            </div>
            <span className="text-2xl font-bold text-neutral-900">{completionPercent}%</span>
          </div>
          <div className="h-3 bg-neutral-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-green-600 transition-all"
              style={{ width: `${completionPercent}%` }}
            />
          </div>
        </motion.div>
      )}

      {/* Overview */}
      {roadmap?.overview && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-8 shadow-sm border border-neutral-100"
        >
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <HiOutlineSparkles className="w-6 h-6 text-blue-600" />
            Career Overview
          </h3>
          <p className="text-neutral-700 leading-relaxed text-base">{roadmap.overview}</p>
        </motion.div>
      )}

      {/* Stages */}
      {roadmap?.stages && roadmap.stages.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl p-8 shadow-sm border border-neutral-100"
        >
          <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
            <HiOutlineChartBar className="w-6 h-6 text-green-600" />
            Career Development Stages
          </h3>
          <div className="space-y-6">
            {roadmap.stages.map((stage, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="border-l-4 border-neutral-900 pl-6 pb-6 relative"
              >
                <div className="absolute -left-3 top-0 w-5 h-5 bg-neutral-900 rounded-full border-4 border-white"></div>
                
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-bold text-lg">{stage.level}</h4>
                  <span className="text-sm font-semibold text-neutral-600 bg-neutral-100 px-3 py-1 rounded-full">
                    ⏱️ {stage.duration}
                  </span>
                </div>

                {stage.skills.length > 0 && (
                  <div className="mb-4">
                    <span className="text-sm font-bold text-neutral-700 block mb-2">📚 Skills to Learn:</span>
                    <div className="flex flex-wrap gap-2">
                      {stage.skills.map((skill) => (
                        <span
                          key={skill}
                          className="px-3 py-1.5 bg-blue-50 text-blue-700 rounded-lg text-xs font-medium border border-blue-200"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {stage.milestones.length > 0 && (
                  <div className="mb-4">
                    <span className="text-sm font-bold text-neutral-700 block mb-2">✅ Key Milestones:</span>
                    <ul className="space-y-2">
                      {stage.milestones.map((milestone, i) => {
                        const key = `${index}-${i}`;
                        const complete = !!progress[key];

                        return (
                          <li key={i} className="flex items-start gap-2 text-sm text-neutral-600">
                            <button
                              onClick={() => toggleMilestone(key)}
                              className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded border text-xs ${
                                complete
                                  ? "border-green-600 bg-green-600 text-white"
                                  : "border-neutral-300 bg-white"
                              }`}
                              aria-label={complete ? "Mark milestone incomplete" : "Mark milestone complete"}
                            >
                              {complete ? "✓" : ""}
                            </button>
                            <span className={complete ? "line-through text-neutral-400" : ""}>{milestone}</span>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                )}

                {stage.resources.length > 0 && (
                  <div>
                    <span className="text-sm font-bold text-neutral-700 block mb-2">📖 Resources:</span>
                    <ul className="space-y-1">
                      {stage.resources.map((resource, i) => (
                        <li key={i} className="text-sm text-neutral-600 flex items-start gap-2">
                          <span className="text-blue-600">→</span>
                          {resource}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Job Roles */}
      {roadmap?.job_roles && roadmap.job_roles.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-2xl p-8 shadow-sm border border-neutral-100"
        >
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <HiOutlineClipboardDocumentList className="w-6 h-6 text-purple-600" />
            Related Job Roles
          </h3>
          <div className="grid md:grid-cols-2 gap-3">
            {roadmap.job_roles.map((role, i) => (
              <div key={i} className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                <p className="text-sm font-semibold text-purple-900">{role}</p>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Technologies */}
      {roadmap?.tools_and_technologies && roadmap.tools_and_technologies.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-2xl p-8 shadow-sm border border-neutral-100"
        >
          <h3 className="text-xl font-bold mb-4">🛠️ Tools & Technologies</h3>
          <div className="flex flex-wrap gap-2">
            {roadmap.tools_and_technologies.map((tool) => (
              <span key={tool} className="px-4 py-2 bg-neutral-100 text-neutral-800 rounded-lg text-sm font-medium border border-neutral-200">
                {tool}
              </span>
            ))}
          </div>
        </motion.div>
      )}

      {/* Growth Paths */}
      {roadmap?.growth_paths && roadmap.growth_paths.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-2xl p-8 shadow-sm border border-neutral-100"
        >
          <h3 className="text-xl font-bold mb-4">🚀 Career Growth Paths</h3>
          <div className="space-y-3">
            {roadmap.growth_paths.map((path, i) => (
              <div key={i} className="flex items-start gap-3 p-4 bg-linear-to-r from-blue-50 to-transparent rounded-lg border border-blue-200">
                <span className="text-lg mt-0.5">→</span>
                <span className="text-neutral-700">{path}</span>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}

// Colleges Tab Component
function CollegesTab({ recommendation }: { recommendation: Recommendation }) {
  const [collegeSearch, setCollegeSearch] = useState("");
  const [locationFilter, setLocationFilter] = useState("");
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
  const locations = useMemo(() => {
    const values = (colleges?.recommendations || [])
      .map((college) => college.location)
      .filter(Boolean);
    return Array.from(new Set(values)).sort();
  }, [colleges?.recommendations]);
  const filteredRecommendations = useMemo(() => {
    return (colleges?.recommendations || []).filter((college) => {
      const query = collegeSearch.toLowerCase().trim();
      const matchesQuery = !query || [
        college.name,
        college.location,
        ...(college.programs || []),
        college.reason || "",
      ].join(" ").toLowerCase().includes(query);
      const matchesLocation = !locationFilter || college.location === locationFilter;

      return matchesQuery && matchesLocation;
    });
  }, [colleges?.recommendations, collegeSearch, locationFilter]);

  if (!recommendation.hasFullDetails || !colleges?.recommendations) {
    return (
      <div className="bg-white rounded-2xl p-12 text-center shadow-sm border border-neutral-100">
        <div className="w-20 h-20 bg-neutral-50 rounded-2xl flex items-center justify-center mx-auto mb-6 border border-neutral-100">
          <HiOutlineAcademicCap className="w-10 h-10 text-neutral-400" />
        </div>
        <h2 className="text-2xl font-bold mb-3">College Recommendations</h2>
        <p className="text-neutral-500 mb-4 max-w-lg mx-auto leading-relaxed">
          Generate your full career roadmap to see personalized college recommendations that align with your career goals.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Recommended Colleges */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-2xl p-8 shadow-sm border border-neutral-100"
      >
        <h3 className="text-2xl font-bold mb-6 flex items-center gap-2">
          <HiOutlineAcademicCap className="w-7 h-7 text-green-600" />
          Top Recommended Colleges
        </h3>
        <div className="mb-6 grid md:grid-cols-2 gap-3">
          <input
            value={collegeSearch}
            onChange={(event) => setCollegeSearch(event.target.value)}
            placeholder="Search college, program, or reason"
            className="w-full rounded-lg border border-neutral-200 px-4 py-3 text-sm outline-none focus:border-neutral-900"
          />
          <select
            value={locationFilter}
            onChange={(event) => setLocationFilter(event.target.value)}
            className="w-full rounded-lg border border-neutral-200 px-4 py-3 text-sm outline-none focus:border-neutral-900"
          >
            <option value="">All locations</option>
            {locations.map((location) => (
              <option key={location} value={location}>{location}</option>
            ))}
          </select>
        </div>
        <div className="grid md:grid-cols-2 gap-6">
          {filteredRecommendations.map((college, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`p-6 rounded-xl border-2 transition-all ${
                index === 0
                  ? "border-green-300 bg-linear-to-br from-green-50 to-white shadow-md"
                  : "border-neutral-200 hover:border-neutral-300 hover:shadow-md"
              }`}
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  {index === 0 && (
                    <span className="px-3 py-1 bg-green-600 text-white text-xs rounded-full font-semibold inline-block mb-2">
                      ⭐ Highly Recommended
                    </span>
                  )}
                  <h4 className="font-bold text-lg">{college.name}</h4>
                </div>
              </div>

              <div className="flex items-center gap-1 text-neutral-600 mb-4">
                <HiOutlineBuildingOffice2 className="w-5 h-5" />
                <span className="text-sm font-medium">{college.location}</span>
              </div>

              {college.programs && college.programs.length > 0 && (
                <div className="mb-4">
                  <span className="text-xs font-bold text-neutral-700 block mb-2">Available Programs:</span>
                  <div className="flex flex-wrap gap-2">
                    {college.programs.slice(0, 4).map((program) => (
                      <span
                        key={program}
                        className="px-3 py-1.5 bg-blue-50 text-blue-700 text-xs rounded-lg font-medium border border-blue-200"
                      >
                        {program}
                      </span>
                    ))}
                    {college.programs.length > 4 && (
                      <span className="px-3 py-1.5 bg-neutral-100 text-neutral-700 text-xs rounded-lg font-medium">
                        +{college.programs.length - 4} more
                      </span>
                    )}
                  </div>
                </div>
              )}

              {college.reason && (
                <div className="p-4 bg-neutral-50 rounded-lg border border-neutral-200">
                  <span className="text-xs font-bold text-neutral-700">Why this college?</span>
                  <p className="text-sm text-neutral-600 mt-2 leading-relaxed">{college.reason}</p>
                </div>
              )}
            </motion.div>
          ))}
        </div>
        {filteredRecommendations.length === 0 && (
          <p className="text-sm text-neutral-500">No colleges match the current filters.</p>
        )}
      </motion.div>

      {/* Alternative Colleges */}
      {colleges.alternatives && colleges.alternatives.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-2xl p-8 shadow-sm border border-neutral-100"
        >
          <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
            <HiOutlineAcademicCap className="w-6 h-6 text-blue-600" />
            Alternative Colleges
          </h3>
          <div className="grid md:grid-cols-3 gap-4">
            {colleges.alternatives.map((college, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.08 }}
                className="p-5 bg-blue-50 rounded-xl border border-blue-200"
              >
                <h4 className="font-semibold text-blue-900">{college.name}</h4>
                <p className="text-sm text-blue-700 flex items-center gap-1 mt-2">
                  <HiOutlineBuildingOffice2 className="w-4 h-4" />
                  {college.location}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}

const reportSectionHeadings = new Set([
  "Career Fit",
  "Key Skills",
  "Education Pathway",
  "Motivation",
]);

function ProjectReportSummary({ summary }: { summary: string }) {
  const sections = summary
    .split(/\n{2,}/)
    .map((section) => section.trim())
    .filter(Boolean)
    .map((section) => {
      const [firstLine, ...bodyLines] = section.split("\n");
      const heading = firstLine.trim();
      const hasKnownHeading = reportSectionHeadings.has(heading);

      return {
        heading: hasKnownHeading ? heading : null,
        body: hasKnownHeading ? bodyLines.join("\n").trim() : section,
      };
    });

  if (sections.length === 0) {
    return null;
  }

  return (
    <div className="space-y-5">
      {sections.map((section, index) => {
        const lines = section.body.split("\n").map((line) => line.trim()).filter(Boolean);
        const allBullets = lines.length > 0 && lines.every((line) => line.startsWith("- "));

        return (
          <section key={`${section.heading || "summary"}-${index}`} className="space-y-2">
            {section.heading && (
              <h4 className="text-base font-bold text-neutral-900">{section.heading}</h4>
            )}
            {allBullets ? (
              <ul className="list-disc space-y-1 pl-5 text-neutral-700 leading-relaxed text-base">
                {lines.map((line) => (
                  <li key={line}>{line.slice(2)}</li>
                ))}
              </ul>
            ) : (
              <p className="text-neutral-700 leading-relaxed text-base whitespace-pre-wrap">
                {section.body}
              </p>
            )}
          </section>
        );
      })}
    </div>
  );
}

// Summary Tab Component
function SummaryTab({
  recommendation,
  onFeedback,
}: {
  recommendation: Recommendation;
  onFeedback: (feedback: "helpful" | "not_helpful", comment: string) => Promise<void>;
}) {
  const [feedbackComment, setFeedbackComment] = useState(recommendation.feedbackComment || "");
  const [savingFeedback, setSavingFeedback] = useState(false);

  const submitFeedback = async (feedback: "helpful" | "not_helpful") => {
    setSavingFeedback(true);
    await onFeedback(feedback, feedbackComment);
    setSavingFeedback(false);
  };

  return (
    <div className="space-y-6">
      {/* Main Summary */}
      {recommendation.summary && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-linear-to-br from-blue-50 to-white rounded-2xl p-8 shadow-sm border border-blue-200"
        >
          <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
            <HiOutlineBookOpen className="w-7 h-7 text-blue-600" />
            Project Report for {recommendation.topCareer}
          </h3>
          <div className="prose prose-neutral max-w-none">
            <ProjectReportSummary summary={recommendation.summary} />
          </div>
        </motion.div>
      )}

      {/* Immediate Actions */}
      {recommendation.immediateActions && recommendation.immediateActions.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl p-8 shadow-sm border border-neutral-100"
        >
          <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
            <HiOutlineClipboardDocumentList className="w-6 h-6 text-orange-600" />
            Next Steps - Immediate Actions
          </h3>
          <div className="space-y-4">
            {recommendation.immediateActions.map((action, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-start gap-4 p-5 bg-orange-50 rounded-xl border border-orange-200"
              >
                <span className="w-8 h-8 rounded-full bg-orange-600 text-white text-sm font-bold flex items-center justify-center shrink-0 mt-0.5">
                  {index + 1}
                </span>
                <span className="text-neutral-700 leading-relaxed pt-1">{action}</span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15 }}
        className="bg-white rounded-2xl p-8 shadow-sm border border-neutral-100"
      >
        <h3 className="text-xl font-bold mb-2">Recommendation Feedback</h3>
        <p className="text-sm text-neutral-500 mb-4">
          Your feedback helps evaluate whether the recommendations are actually useful.
        </p>
        <textarea
          value={feedbackComment}
          onChange={(event) => setFeedbackComment(event.target.value)}
          placeholder="Optional note about what felt right or wrong"
          className="w-full min-h-24 rounded-xl border border-neutral-200 px-4 py-3 text-sm outline-none focus:border-neutral-900"
        />
        <div className="mt-4 flex flex-wrap gap-3">
          <button
            onClick={() => submitFeedback("helpful")}
            disabled={savingFeedback}
            className={`rounded-lg px-5 py-2.5 text-sm font-semibold ${
              recommendation.userFeedback === "helpful"
                ? "bg-green-600 text-white"
                : "bg-green-50 text-green-700 border border-green-200"
            } disabled:opacity-60`}
          >
            Helpful
          </button>
          <button
            onClick={() => submitFeedback("not_helpful")}
            disabled={savingFeedback}
            className={`rounded-lg px-5 py-2.5 text-sm font-semibold ${
              recommendation.userFeedback === "not_helpful"
                ? "bg-red-600 text-white"
                : "bg-red-50 text-red-700 border border-red-200"
            } disabled:opacity-60`}
          >
            Not Helpful
          </button>
          {recommendation.feedbackCreatedAt && (
            <span className="self-center text-sm text-neutral-500">
              Saved {new Date(recommendation.feedbackCreatedAt).toLocaleString()}
            </span>
          )}
        </div>
      </motion.div>

      {/* Additional Context */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-2xl p-8 shadow-sm border border-neutral-100"
      >
        <h3 className="text-xl font-bold mb-4">📌 How This Recommendation Was Generated</h3>
        <div className="space-y-3 text-neutral-700 text-sm leading-relaxed">
          <p>
            Our AI analyzed your academic background, skills, interests, and specialization to identify the most suitable careers for you. Each recommendation includes:
          </p>
          <ul className="list-disc list-inside space-y-2 text-neutral-600">
            <li>Confidence scores indicating how well each career matches your profile</li>
            <li>Detailed career roadmaps with progressive stages and skill requirements</li>
            <li>Personalized college recommendations based on your career path</li>
            <li>Immediate actionable steps to start your journey</li>
            <li>Growth opportunities and advancement paths within each field</li>
          </ul>
          <p className="text-neutral-500 italic mt-4">
            Use this information to make informed decisions about your future and take concrete steps toward your chosen career path.
          </p>
        </div>
      </motion.div>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-linear-to-br from-neutral-50 to-neutral-100 flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-neutral-900 border-t-transparent rounded-full animate-spin"></div>
      </div>
    }>
      <DashboardContent />
    </Suspense>
  );
}
