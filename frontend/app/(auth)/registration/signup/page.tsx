"use client";

import Link from "next/link";
import { useState, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaRegEye, FaRegEyeSlash } from "react-icons/fa";
import {
  HiOutlineComputerDesktop,
  HiOutlineHeart,
  HiOutlineBuildingOffice2,
  HiOutlineCog6Tooth,
  HiOutlinePaintBrush,
  HiOutlineAcademicCap,
  HiOutlineTrophy,
  HiOutlineChatBubbleLeftRight,
  HiOutlineBeaker,
  HiOutlineScale,
  HiOutlineArrowLeft,
  HiOutlineCheck,
  HiOutlineMagnifyingGlass,
} from "react-icons/hi2";

// Types
interface FormData {
  email: string;
  password: string;
  confirmPassword: string;
  fullName: string;
  gender: string;
  dateOfBirth: string;
  cityRegion: string;
  courseCategory: string;
  course: string;
  specialization: string;
  schoolCollegeName: string;
  cgpa: string;
  interests: string[];
  technicalSkills: string[];
  softSkills: string[];
  hasCertification: boolean;
  certifications: string;
  careerLifestyle: string;
  workEnvironment: string;
  locationPreference: string;
  learningStyle: string;
}

const initialFormData: FormData = {
  email: "",
  password: "",
  confirmPassword: "",
  fullName: "",
  gender: "",
  dateOfBirth: "",
  cityRegion: "",
  courseCategory: "",
  course: "",
  specialization: "",
  schoolCollegeName: "",
  cgpa: "",
  interests: [],
  technicalSkills: [],
  softSkills: [],
  hasCertification: false,
  certifications: "",
  careerLifestyle: "",
  workEnvironment: "",
  locationPreference: "",
  learningStyle: "",
};

// Gender options
const genderOptions = ["Male", "Female", "Other", "Prefer not to say"];

// Course categories matching the AI model
const courseCategories = {
  engineering: {
    label: "Engineering",
    courses: ["B.Tech", "B.E", "M.Tech", "M.E", "Diploma in Engineering"],
  },
  science: {
    label: "Science",
    courses: ["B.Sc", "M.Sc", "Biotechnology", "B.Sc (Hons)"],
  },
  commerce: {
    label: "Commerce",
    courses: ["B.Com", "M.Com", "B.Com (Hons)", "Chartered Accountancy (CA)"],
  },
  business: {
    label: "Business & Management",
    courses: ["BBA", "MBA", "BMS", "PGDM", "BBM"],
  },
  computer: {
    label: "Computer Applications",
    courses: ["BCA", "MCA", "B.Sc IT", "M.Sc IT"],
  },
  arts: {
    label: "Arts & Humanities",
    courses: ["BA", "MA", "BA (Hons)", "Economics", "Psychology", "Sociology"],
  },
  law: {
    label: "Law",
    courses: ["BALLB", "LLB", "LLM", "BA LLB", "BBA LLB"],
  },
  medical: {
    label: "Medical & Healthcare",
    courses: ["MBBS", "BDS", "B.Pharmacy", "B.Sc Nursing", "BAMS", "BHMS", "Pharm.D"],
  },
  media: {
    label: "Media & Journalism",
    courses: ["BMM", "BJMC", "BA Journalism", "Mass Communication"],
  },
  architecture: {
    label: "Architecture & Design",
    courses: ["B.Arch", "M.Arch", "B.Des", "M.Des"],
  },
  hospitality: {
    label: "Hospitality & Tourism",
    courses: ["BHM", "BHMCT", "Hotel Management", "Tourism Management"],
  },
  other: {
    label: "Other",
    courses: ["Other"],
  },
};

// Interest categories matching the AI model
const interestCategories = [
  { id: "technology", label: "Technology", icon: HiOutlineComputerDesktop },
  { id: "healthcare", label: "Healthcare", icon: HiOutlineHeart },
  { id: "business", label: "Business", icon: HiOutlineBuildingOffice2 },
  { id: "engineering", label: "Engineering", icon: HiOutlineCog6Tooth },
  { id: "design", label: "Design & Arts", icon: HiOutlinePaintBrush },
  { id: "teaching", label: "Teaching", icon: HiOutlineAcademicCap },
  { id: "research", label: "Research", icon: HiOutlineBeaker },
  { id: "data_analytics", label: "Data Analytics", icon: HiOutlineComputerDesktop },
  { id: "financial_analysis", label: "Finance", icon: HiOutlineBuildingOffice2 },
  { id: "marketing", label: "Marketing", icon: HiOutlineChatBubbleLeftRight },
  { id: "sales", label: "Sales", icon: HiOutlineTrophy },
  { id: "law", label: "Law & Government", icon: HiOutlineScale },
  { id: "entrepreneurship", label: "Entrepreneurship", icon: HiOutlineBuildingOffice2 },
  { id: "web", label: "Web Development", icon: HiOutlineComputerDesktop },
  { id: "gaming", label: "Gaming", icon: HiOutlineTrophy },
  { id: "journalism", label: "Media & Journalism", icon: HiOutlineChatBubbleLeftRight },
];

const careerLifestyleOptions = ["High income potential", "Work-life balance", "Job security", "Creative freedom", "Making a difference"];
const workEnvironmentOptions = ["Remote / Work from home", "Office-based", "Hybrid", "Outdoor / Field work", "No preference"];
const locationPreferenceOptions = ["Stay in my city", "Willing to relocate nationally", "Open to international opportunities", "Prefer remote work"];
const learningStyleOptions = ["Self-paced online learning", "Classroom / Instructor-led", "Hands-on / Practical experience", "Mentorship", "Mix of all"];

// College interface
interface College {
  name: string;
  location: string;
  university: string;
  courseOffered: string;
}

const footerQuotes = [
  "Your account lets you save career options, track progress, and access personalized insights.",
  "Your background helps our AI understand your strengths so we can recommend careers that fit you.",
  "Your interests reveal what excites you. Your skills show what you're already good at. Together, they shape your future career.",
  "These choices help us match you with careers that align with the future you want.",
  "Everything looks great! You're ready to explore careers tailored to your skills, interests, and goals.",
];

// Animation variants
const pageVariants = {
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.08,
    },
  },
};

const staggerItem = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
};

const progressDotVariants = {
  initial: { scale: 0.8, opacity: 0 },
  animate: (i: number) => ({
    scale: 1,
    opacity: 1,
    transition: { delay: i * 0.1, type: "spring" as const, stiffness: 300, damping: 20 },
  }),
};

export default function Signup() {
  const [currentStep, setCurrentStep] = useState(1);
  const [currentSubStep, setCurrentSubStep] = useState(0);
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [colleges, setColleges] = useState<College[]>([]);
  const [collegeSearch, setCollegeSearch] = useState("");
  const [showCollegeDropdown, setShowCollegeDropdown] = useState(false);

  const totalSteps = 5;

  // Load colleges from CSV
  useEffect(() => {
    const loadColleges = async () => {
      try {
        const response = await fetch("/Colleges in Nepal.csv");
        const text = await response.text();
        const lines = text.split("\n").slice(1); // Skip header
        const parsedColleges: College[] = lines
          .filter(line => line.trim())
          .map(line => {
            const [name, location, university, courseOffered] = line.split(",").map(s => s?.trim() || "");
            return { name, location, university, courseOffered };
          })
          .filter(c => c.name);
        setColleges(parsedColleges);
      } catch (error) {
        console.error("Failed to load colleges:", error);
      }
    };
    loadColleges();
  }, []);

  // Filter colleges based on search
  const filteredColleges = useMemo(() => {
    if (!collegeSearch) return colleges.slice(0, 10);
    const searchLower = collegeSearch.toLowerCase();
    return colleges
      .filter(c => 
        c.name.toLowerCase().includes(searchLower) ||
        c.location.toLowerCase().includes(searchLower) ||
        c.university.toLowerCase().includes(searchLower)
      )
      .slice(0, 10);
  }, [colleges, collegeSearch]);

  const handleInputChange = (field: keyof FormData, value: string | string[] | boolean) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    if (currentStep === 1) {
      setCurrentStep(2);
      setCurrentSubStep(0);
    } else if (currentStep === 2) {
      if (currentSubStep === 0) setCurrentSubStep(1);
      else { setCurrentStep(3); setCurrentSubStep(0); }
    } else if (currentStep === 3) {
      // Step 3 now has only 2 substeps: intro (0) and combined interests/skills form (1)
      if (currentSubStep === 0) setCurrentSubStep(1);
      else { setCurrentStep(4); setCurrentSubStep(0); }
    } else if (currentStep === 4) {
      if (currentSubStep === 0) setCurrentSubStep(1);
      else { setCurrentStep(5); setCurrentSubStep(0); }
    } else if (currentStep === 5) {
      if (currentSubStep === 0) setCurrentSubStep(1);
      else handleSubmit();
    }
  };

  const handleBack = () => {
    if (currentStep === 1) return;

    if (currentSubStep > 0) {
      setCurrentSubStep(currentSubStep - 1);
    } else {
      if (currentStep === 2) setCurrentStep(1);
      else if (currentStep === 3) { setCurrentStep(2); setCurrentSubStep(1); }
      else if (currentStep === 4) { setCurrentStep(3); setCurrentSubStep(1); }
      else if (currentStep === 5) { setCurrentStep(4); setCurrentSubStep(1); }
    }
  };

  const handleSubmit = () => {
    console.log("Form submitted:", formData);
  };

  const getButtonText = () => {
    if (currentStep === 1) return "Create Account";
    if (currentStep === 5 && currentSubStep === 1) return "Complete Setup";
    return "Next";
  };

  const getFooterQuote = () => footerQuotes[currentStep - 1] || footerQuotes[0];
  const getStepKey = () => `${currentStep}-${currentSubStep}`;

  // Step 1 - Account Creation
  const renderStep1 = () => (
    <motion.div
      key="step1"
      variants={staggerContainer}
      initial="initial"
      animate="animate"
      className="w-full flex-1 flex flex-col md:flex-row gap-8 md:gap-16 lg:gap-32 px-8 md:px-16 lg:px-32 xl:px-64 items-center justify-center"
    >
      <div className="w-full md:w-2/5 space-y-4">
        <motion.p variants={staggerItem} className="text-2xl md:text-3xl font-semibold text-neutral-600">
          Step 1
        </motion.p>
        <motion.h1 variants={staggerItem} className="text-3xl md:text-4xl lg:text-5xl font-bold leading-tight">
          Create Your Skill Lantern Account
        </motion.h1>
        <motion.p variants={staggerItem} className="text-gray-600 text-lg">
          Start by creating your Skill Lantern account. You&apos;ll use this to
          access your recommendations and dashboard.
        </motion.p>
      </div>
      <motion.div variants={staggerItem} className="w-full md:w-2/5">
        <form className="space-y-6">
          <motion.div variants={staggerItem} className="w-full gap-2 flex flex-col">
            <label className="font-medium text-sm">Email</label>
            <input
              type="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={(e) => handleInputChange("email", e.target.value)}
              className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all"
              required
            />
          </motion.div>
          <motion.div variants={staggerItem} className="w-full gap-2 flex flex-col">
            <label className="font-medium text-sm">Password</label>
            <div className="w-full flex items-center border-b-2 border-neutral-300 focus-within:border-neutral-900 transition-all">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                value={formData.password}
                onChange={(e) => handleInputChange("password", e.target.value)}
                className="w-full px-4 py-3 bg-transparent outline-none"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="p-2 text-neutral-500 hover:text-neutral-700 transition-colors"
              >
                {showPassword ? <FaRegEyeSlash size={18} /> : <FaRegEye size={18} />}
              </button>
            </div>
          </motion.div>
          <motion.div variants={staggerItem} className="w-full gap-2 flex flex-col">
            <label className="font-medium text-sm">Confirm Password</label>
            <div className="w-full flex items-center border-b-2 border-neutral-300 focus-within:border-neutral-900 transition-all">
              <input
                type={showConfirmPassword ? "text" : "password"}
                placeholder="Confirm your password"
                value={formData.confirmPassword}
                onChange={(e) => handleInputChange("confirmPassword", e.target.value)}
                className="w-full px-4 py-3 bg-transparent outline-none"
                required
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="p-2 text-neutral-500 hover:text-neutral-700 transition-colors"
              >
                {showConfirmPassword ? <FaRegEyeSlash size={18} /> : <FaRegEye size={18} />}
              </button>
            </div>
          </motion.div>
        </form>
      </motion.div>
    </motion.div>
  );

  // Step Intro Component
  const renderStepIntro = (step: number, title: string, subtitle: string, gifSrc: string) => (
    <motion.div
      key={`step${step}-intro`}
      variants={staggerContainer}
      initial="initial"
      animate="animate"
      className="w-full flex-1 flex flex-col md:flex-row gap-8 md:gap-16 lg:gap-32 px-8 md:px-16 lg:px-32 xl:px-64 items-center justify-center"
    >
      <div className="w-full md:w-2/5 space-y-4">
        <motion.p variants={staggerItem} className="text-2xl md:text-3xl font-semibold text-neutral-600">
          Step {step}
        </motion.p>
        <motion.h1 variants={staggerItem} className="text-3xl md:text-4xl lg:text-5xl font-bold leading-tight">
          {title}
        </motion.h1>
        <motion.p variants={staggerItem} className="text-gray-600 text-lg">
          {subtitle}
        </motion.p>
      </div>
      <motion.div
        variants={staggerItem}
        className="w-full md:w-2/5 flex items-center justify-center"
      >
        <div className="w-64 h-64 relative">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={gifSrc}
            alt={title}
            className="w-full h-full object-contain"
          />
        </div>
      </motion.div>
    </motion.div>
  );

  // Step 2 Form - Personal & Academic Details
  const renderStep2Form = () => (
    <motion.div
      key="step2-form"
      variants={staggerContainer}
      initial="initial"
      animate="animate"
      className="w-full flex-1 flex flex-col px-8 md:px-16 lg:px-32 xl:px-64 py-8 overflow-y-auto"
    >
      <div className="max-w-2xl mx-auto w-full space-y-10">
        {/* Personal Details */}
        <motion.div variants={staggerItem} className="space-y-6">
          <h2 className="text-2xl font-bold text-center">Personal Details</h2>
          <div className="space-y-4">
            <div className="w-full gap-2 flex flex-col">
              <label className="font-medium text-sm">Full Name</label>
              <input
                type="text"
                placeholder="Enter your full name"
                value={formData.fullName}
                onChange={(e) => handleInputChange("fullName", e.target.value)}
                className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all"
              />
            </div>
            <div className="w-full gap-2 flex flex-col">
              <label className="font-medium text-sm">Gender</label>
              <select
                value={formData.gender}
                onChange={(e) => handleInputChange("gender", e.target.value)}
                className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all appearance-none cursor-pointer"
              >
                <option value="">Select your gender</option>
                {genderOptions.map((gender) => (
                  <option key={gender} value={gender}>{gender}</option>
                ))}
              </select>
            </div>
            <div className="w-full gap-2 flex flex-col">
              <label className="font-medium text-sm">Date of Birth</label>
              <input
                type="date"
                value={formData.dateOfBirth}
                onChange={(e) => handleInputChange("dateOfBirth", e.target.value)}
                className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all"
              />
            </div>
            <div className="w-full gap-2 flex flex-col">
              <label className="font-medium text-sm">City / Region</label>
              <input
                type="text"
                placeholder="Enter your city / region"
                value={formData.cityRegion}
                onChange={(e) => handleInputChange("cityRegion", e.target.value)}
                className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all"
              />
            </div>
          </div>
        </motion.div>

        {/* Academic Information */}
        <motion.div variants={staggerItem} className="space-y-6">
          <h2 className="text-2xl font-bold text-center">Academic Information</h2>
          <div className="space-y-4">
            <div className="w-full gap-2 flex flex-col">
              <label className="font-medium text-sm">Course Category</label>
              <select
                value={formData.courseCategory}
                onChange={(e) => {
                  handleInputChange("courseCategory", e.target.value);
                  handleInputChange("course", ""); // Reset course when category changes
                }}
                className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all appearance-none cursor-pointer"
              >
                <option value="">Select course category</option>
                {Object.entries(courseCategories).map(([key, category]) => (
                  <option key={key} value={key}>{category.label}</option>
                ))}
              </select>
            </div>
            {formData.courseCategory && (
              <div className="w-full gap-2 flex flex-col">
                <label className="font-medium text-sm">Course / Degree</label>
                <select
                  value={formData.course}
                  onChange={(e) => handleInputChange("course", e.target.value)}
                  className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all appearance-none cursor-pointer"
                >
                  <option value="">Select your course</option>
                  {courseCategories[formData.courseCategory as keyof typeof courseCategories]?.courses.map((course) => (
                    <option key={course} value={course}>{course}</option>
                  ))}
                </select>
              </div>
            )}
            <div className="w-full gap-2 flex flex-col">
              <label className="font-medium text-sm">Specialization (Optional)</label>
              <input
                type="text"
                placeholder="e.g., Computer Science, Finance, Marketing"
                value={formData.specialization}
                onChange={(e) => handleInputChange("specialization", e.target.value)}
                className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all"
              />
            </div>
            <div className="w-full gap-2 flex flex-col relative">
              <label className="font-medium text-sm">School / College Name</label>
              <div className="relative">
                <div className="flex items-center border-b-2 border-neutral-300 focus-within:border-neutral-900 transition-all">
                  <HiOutlineMagnifyingGlass className="text-neutral-400 ml-2" size={18} />
                  <input
                    type="text"
                    placeholder="Search or type your college name"
                    value={collegeSearch || formData.schoolCollegeName}
                    onChange={(e) => {
                      setCollegeSearch(e.target.value);
                      handleInputChange("schoolCollegeName", e.target.value);
                      setShowCollegeDropdown(true);
                    }}
                    onFocus={() => setShowCollegeDropdown(true)}
                    onBlur={() => setTimeout(() => setShowCollegeDropdown(false), 200)}
                    className="w-full px-4 py-3 bg-transparent focus:outline-none"
                  />
                </div>
                {showCollegeDropdown && filteredColleges.length > 0 && (
                  <div className="absolute z-50 w-full bg-white border border-neutral-200 rounded-lg shadow-lg mt-1 max-h-60 overflow-y-auto">
                    {filteredColleges.map((college, idx) => (
                      <button
                        key={`${college.name}-${idx}`}
                        type="button"
                        className="w-full px-4 py-3 text-left hover:bg-neutral-100 transition-colors border-b border-neutral-100 last:border-0"
                        onClick={() => {
                          handleInputChange("schoolCollegeName", college.name);
                          setCollegeSearch(college.name);
                          setShowCollegeDropdown(false);
                        }}
                      >
                        <div className="font-medium text-sm">{college.name}</div>
                        <div className="text-xs text-neutral-500">{college.location} • {college.university}</div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
            <div className="w-full gap-2 flex flex-col">
              <label className="font-medium text-sm">CGPA / Percentage</label>
              <p className="text-xs text-gray-500">Enter CGPA (0-10) or Percentage (0-100)</p>
              <input
                type="text"
                placeholder="e.g., 8.5 or 85%"
                value={formData.cgpa}
                onChange={(e) => handleInputChange("cgpa", e.target.value)}
                className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all"
              />
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );

  // Step 3 - Combined Interests & Skills (Single Page)
  const renderStep3Combined = () => (
    <motion.div
      key="step3-combined"
      variants={staggerContainer}
      initial="initial"
      animate="animate"
      className="w-full flex-1 flex flex-col px-8 md:px-16 lg:px-32 xl:px-64 py-8 overflow-y-auto"
    >
      <div className="max-w-2xl mx-auto w-full space-y-10">
        {/* Interests Section - Dropdown */}
        <motion.div variants={staggerItem} className="space-y-4">
          <div className="space-y-2">
            <h2 className="text-2xl font-bold">Interests</h2>
            <p className="text-gray-600 text-sm">Select your primary area of interest:</p>
          </div>
          <select
            value={formData.interests[0] || ""}
            onChange={(e) => handleInputChange("interests", e.target.value ? [e.target.value] : [])}
            className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all appearance-none cursor-pointer"
          >
            <option value="">Select your interest</option>
            {interestCategories.map((category) => (
              <option key={category.id} value={category.id}>{category.label}</option>
            ))}
          </select>
        </motion.div>

        {/* Skills Section - Input Fields */}
        <motion.div variants={staggerItem} className="space-y-6">
          <div className="space-y-2">
            <h2 className="text-2xl font-bold">Skills</h2>
            <p className="text-gray-600 text-sm">Enter your skills (comma separated):</p>
          </div>
          
          {/* Technical Skills - Input */}
          <div className="w-full gap-2 flex flex-col">
            <label className="font-medium text-sm">Technical Skills</label>
            <input
              type="text"
              placeholder="e.g., Python, JavaScript, Excel, AutoCAD"
              value={formData.technicalSkills.join(", ")}
              onChange={(e) => handleInputChange("technicalSkills", e.target.value.split(",").map(s => s.trim()).filter(s => s))}
              className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all"
            />
          </div>

          {/* Soft Skills - Input */}
          <div className="w-full gap-2 flex flex-col">
            <label className="font-medium text-sm">Soft Skills</label>
            <input
              type="text"
              placeholder="e.g., Communication, Leadership, Teamwork"
              value={formData.softSkills.join(", ")}
              onChange={(e) => handleInputChange("softSkills", e.target.value.split(",").map(s => s.trim()).filter(s => s))}
              className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all"
            />
          </div>
        </motion.div>

        {/* Certifications */}
        <motion.div variants={staggerItem} className="space-y-4">
          <h2 className="text-2xl font-bold">Certifications</h2>
          <div className="space-y-4">
            <div className="w-full gap-2 flex flex-col">
              <label className="font-medium text-sm">Do you have any certifications?</label>
              <div className="flex gap-4 mt-2">
                <motion.button
                  type="button"
                  onClick={() => handleInputChange("hasCertification", true)}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className={`px-6 py-2 rounded-full border-2 transition-all ${
                    formData.hasCertification
                      ? "border-neutral-900 bg-neutral-900 text-white"
                      : "border-neutral-300 hover:border-neutral-500"
                  }`}
                >
                  Yes
                </motion.button>
                <motion.button
                  type="button"
                  onClick={() => handleInputChange("hasCertification", false)}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className={`px-6 py-2 rounded-full border-2 transition-all ${
                    !formData.hasCertification
                      ? "border-neutral-900 bg-neutral-900 text-white"
                      : "border-neutral-300 hover:border-neutral-500"
                  }`}
                >
                  No
                </motion.button>
              </div>
            </div>
            {formData.hasCertification && (
              <div className="w-full gap-2 flex flex-col">
                <label className="font-medium text-sm">List your certifications</label>
                <input
                  type="text"
                  placeholder="e.g., AWS Certified, Google Analytics, Python Professional"
                  value={formData.certifications}
                  onChange={(e) => handleInputChange("certifications", e.target.value)}
                  className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all"
                />
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </motion.div>
  );

  // Step 4 - Preferences Form
  const renderStep4Form = () => (
    <motion.div
      key="step4-form"
      variants={staggerContainer}
      initial="initial"
      animate="animate"
      className="w-full flex-1 flex flex-col px-8 md:px-16 lg:px-32 xl:px-64 py-8 overflow-y-auto"
    >
      <div className="max-w-2xl mx-auto w-full space-y-8">
        <motion.div variants={staggerItem} className="w-full gap-2 flex flex-col">
          <label className="font-medium text-sm">Career Lifestyle Preferences</label>
          <p className="text-xs text-gray-500">Which is more important to you?</p>
          <select
            value={formData.careerLifestyle}
            onChange={(e) => handleInputChange("careerLifestyle", e.target.value)}
            className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all appearance-none cursor-pointer"
          >
            <option value="">Select your preference</option>
            {careerLifestyleOptions.map((option) => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </motion.div>
        <motion.div variants={staggerItem} className="w-full gap-2 flex flex-col">
          <label className="font-medium text-sm">Work Environment Preference</label>
          <select
            value={formData.workEnvironment}
            onChange={(e) => handleInputChange("workEnvironment", e.target.value)}
            className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all appearance-none cursor-pointer"
          >
            <option value="">Select your preference</option>
            {workEnvironmentOptions.map((option) => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </motion.div>
        <motion.div variants={staggerItem} className="w-full gap-2 flex flex-col">
          <label className="font-medium text-sm">Location Preference</label>
          <select
            value={formData.locationPreference}
            onChange={(e) => handleInputChange("locationPreference", e.target.value)}
            className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all appearance-none cursor-pointer"
          >
            <option value="">Select your preference</option>
            {locationPreferenceOptions.map((option) => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </motion.div>
        <motion.div variants={staggerItem} className="w-full gap-2 flex flex-col">
          <label className="font-medium text-sm">Learning Style</label>
          <select
            value={formData.learningStyle}
            onChange={(e) => handleInputChange("learningStyle", e.target.value)}
            className="w-full px-4 py-3 border-b-2 border-neutral-300 bg-transparent focus:outline-none focus:border-neutral-900 transition-all appearance-none cursor-pointer"
          >
            <option value="">Select your preference</option>
            {learningStyleOptions.map((option) => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </motion.div>
      </div>
    </motion.div>
  );

  // Step 5 - Review All Information
  const renderStep5Review = () => {
    const ReviewItem = ({ label, value }: { label: string; value: string }) => (
      <div className="flex flex-col sm:flex-row sm:justify-between py-3 border-b border-neutral-200 last:border-0">
        <span className="text-neutral-500 text-sm">{label}</span>
        <span className="font-medium text-neutral-900">{value || <span className="text-neutral-400 italic">Not provided</span>}</span>
      </div>
    );

    return (
      <motion.div
        key="step5-review"
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="w-full flex-1 flex flex-col px-8 md:px-16 lg:px-32 xl:px-64 py-8 overflow-y-auto"
      >
        <div className="max-w-3xl mx-auto w-full space-y-8">
          {/* Header */}
          <motion.div variants={staggerItem} className="text-center space-y-2">
            <h1 className="text-3xl md:text-4xl font-bold">Review Your Information</h1>
            <p className="text-gray-600">Please review your details before we generate your personalized career recommendations.</p>
          </motion.div>

          {/* Account Information */}
          <motion.div variants={staggerItem} className="bg-white rounded-2xl p-6 shadow-sm border border-neutral-200">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <span className="w-8 h-8 bg-neutral-900 text-white rounded-lg flex items-center justify-center text-sm">1</span>
              Account Information
            </h3>
            <ReviewItem label="Email" value={formData.email} />
          </motion.div>

          {/* Personal Details */}
          <motion.div variants={staggerItem} className="bg-white rounded-2xl p-6 shadow-sm border border-neutral-200">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <span className="w-8 h-8 bg-neutral-900 text-white rounded-lg flex items-center justify-center text-sm">2</span>
              Personal Details
            </h3>
            <ReviewItem label="Full Name" value={formData.fullName} />
            <ReviewItem label="Gender" value={formData.gender} />
            <ReviewItem label="Date of Birth" value={formData.dateOfBirth} />
            <ReviewItem label="City / Region" value={formData.cityRegion} />
          </motion.div>

          {/* Academic Information */}
          <motion.div variants={staggerItem} className="bg-white rounded-2xl p-6 shadow-sm border border-neutral-200">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <span className="w-8 h-8 bg-neutral-900 text-white rounded-lg flex items-center justify-center text-sm">2</span>
              Academic Information
            </h3>
            <ReviewItem label="Course Category" value={courseCategories[formData.courseCategory as keyof typeof courseCategories]?.label || formData.courseCategory} />
            <ReviewItem label="Course / Degree" value={formData.course} />
            <ReviewItem label="Specialization" value={formData.specialization} />
            <ReviewItem label="School / College" value={formData.schoolCollegeName} />
            <ReviewItem label="CGPA / Percentage" value={formData.cgpa} />
          </motion.div>

          {/* Interests */}
          <motion.div variants={staggerItem} className="bg-white rounded-2xl p-6 shadow-sm border border-neutral-200">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <span className="w-8 h-8 bg-neutral-900 text-white rounded-lg flex items-center justify-center text-sm">3</span>
              Interests
            </h3>
            {formData.interests.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {formData.interests.map((id) => {
                  const category = interestCategories.find((c) => c.id === id);
                  if (!category) return null;
                  const Icon = category.icon;
                  return (
                    <span
                      key={id}
                      className="inline-flex items-center gap-2 px-3 py-2 bg-neutral-100 rounded-lg text-sm font-medium"
                    >
                      <Icon size={16} />
                      {category.label}
                    </span>
                  );
                })}
              </div>
            ) : (
              <p className="text-neutral-400 italic">No interests selected</p>
            )}
          </motion.div>

          {/* Skills */}
          <motion.div variants={staggerItem} className="bg-white rounded-2xl p-6 shadow-sm border border-neutral-200">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <span className="w-8 h-8 bg-neutral-900 text-white rounded-lg flex items-center justify-center text-sm">3</span>
              Skills
            </h3>
            <div className="space-y-3">
              <div>
                <span className="text-sm text-neutral-500">Technical Skills:</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {formData.technicalSkills.length > 0 ? (
                    formData.technicalSkills.map((skill) => (
                      <span key={skill} className="px-2 py-1 bg-neutral-100 rounded text-sm">{skill}</span>
                    ))
                  ) : (
                    <span className="text-neutral-400 italic">None selected</span>
                  )}
                </div>
              </div>
              <div>
                <span className="text-sm text-neutral-500">Soft Skills:</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {formData.softSkills.length > 0 ? (
                    formData.softSkills.map((skill) => (
                      <span key={skill} className="px-2 py-1 bg-neutral-100 rounded text-sm">{skill}</span>
                    ))
                  ) : (
                    <span className="text-neutral-400 italic">None selected</span>
                  )}
                </div>
              </div>
            </div>
          </motion.div>

          {/* Certifications */}
          <motion.div variants={staggerItem} className="bg-white rounded-2xl p-6 shadow-sm border border-neutral-200">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <span className="w-8 h-8 bg-neutral-900 text-white rounded-lg flex items-center justify-center text-sm">3</span>
              Certifications
            </h3>
            <ReviewItem label="Has Certifications" value={formData.hasCertification ? "Yes" : "No"} />
            {formData.hasCertification && <ReviewItem label="Certifications" value={formData.certifications} />}
          </motion.div>

          {/* Future Goals & Preferences */}
          <motion.div variants={staggerItem} className="bg-white rounded-2xl p-6 shadow-sm border border-neutral-200">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <span className="w-8 h-8 bg-neutral-900 text-white rounded-lg flex items-center justify-center text-sm">4</span>
              Future Goals & Preferences
            </h3>
            <ReviewItem label="Career Lifestyle" value={formData.careerLifestyle} />
            <ReviewItem label="Work Environment" value={formData.workEnvironment} />
            <ReviewItem label="Location Preference" value={formData.locationPreference} />
            <ReviewItem label="Learning Style" value={formData.learningStyle} />
          </motion.div>

          {/* Ready Message */}
          <motion.div variants={staggerItem} className="text-center py-6 space-y-2">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
              className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <HiOutlineCheck className="w-8 h-8 text-green-600" />
            </motion.div>
            <h3 className="text-xl font-bold text-neutral-900">You&apos;re all set!</h3>
            <p className="text-neutral-600">Click &quot;Complete Setup&quot; to generate your personalized career recommendations.</p>
          </motion.div>
        </div>
      </motion.div>
    );
  };

  // Content Router
  const renderContent = () => {
    if (currentStep === 1) return renderStep1();
    if (currentStep === 2) {
      return currentSubStep === 0
        ? renderStepIntro(2, "Tell Us About Yourself", "Share your basic details and academic background so we can understand where you are in your learning journey.", "/step2.gif")
        : renderStep2Form();
    }
    if (currentStep === 3) {
      // Step 3 now has only intro (0) and combined interests/skills form (1)
      return currentSubStep === 0
        ? renderStepIntro(3, "Share Your Interests & Skills", "Help us learn what you enjoy and what you're good at. This helps our AI connect you with careers that match your strengths.", "/step3.gif")
        : renderStep3Combined();
    }
    if (currentStep === 4) {
      return currentSubStep === 0
        ? renderStepIntro(4, "Define Your Future Goals & Preferences", "Tell us the kind of future you want so we can guide you toward careers that fit your preferences and ambitions.", "/step4.gif")
        : renderStep4Form();
    }
    if (currentStep === 5) {
      return currentSubStep === 0
        ? renderStepIntro(5, "Review & Complete Setup", "Take a final look at your information before we generate your personalized career recommendations.", "/step5.gif")
        : renderStep5Review();
    }
    return null;
  };

  return (
    <main className="min-h-screen w-full">
      <div className="h-screen flex flex-col items-center justify-between overflow-hidden">
        {/* Navigation */}
        <nav className="flex w-full justify-between items-center h-16 md:h-20 px-6 md:px-20 shrink-0">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-neutral-900 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">SL</span>
            </div>
            <span className="text-xl font-semibold tracking-tight">Skill Lantern</span>
          </Link>
          {currentStep > 1 && (
            <motion.button
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              onClick={handleBack}
              className="flex items-center gap-2 text-neutral-700 hover:text-neutral-900 transition-colors cursor-pointer"
            >
              <HiOutlineArrowLeft size={18} />
              <span>Back</span>
            </motion.button>
          )}
        </nav>

        {/* Progress Indicator */}
        <div className="w-full px-6 md:px-20 shrink-0">
          <div className="flex items-center justify-center gap-2 mb-4">
            {Array.from({ length: totalSteps }).map((_, index) => (
              <motion.div
                key={index}
                custom={index}
                variants={progressDotVariants}
                initial="initial"
                animate="animate"
                className={`h-1.5 rounded-full transition-all duration-300 ${
                  index + 1 <= currentStep
                    ? "bg-neutral-900 w-12"
                    : "bg-neutral-300 w-8"
                }`}
              />
            ))}
          </div>
        </div>

        {/* Main Content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={getStepKey()}
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={{ duration: 0.4, ease: "easeInOut" }}
            className="flex-1 w-full overflow-y-auto flex"
          >
            {renderContent()}
          </motion.div>
        </AnimatePresence>

        {/* Footer */}
        <footer className="flex justify-between items-center border-t border-neutral-200 h-16 md:h-20 px-6 md:px-20 w-full shrink-0">
          <p className="text-gray-500 text-sm hidden md:block max-w-xl">
            &quot;{getFooterQuote()}&quot;
          </p>
          <motion.button
            onClick={handleNext}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="btn-primary flex items-center gap-2 ml-auto cursor-pointer"
          >
            {getButtonText()}
            {currentStep === 5 && currentSubStep === 1 && <HiOutlineCheck size={18} />}
          </motion.button>
        </footer>
      </div>
    </main>
  );
}
