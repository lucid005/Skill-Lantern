"use client";

import Image from "next/image";
import Link from "next/link";
import { FaArrowRight } from "react-icons/fa6";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

export default function Home() {
  const accordionItems = [
    {
      id: "item-1",
      title: "Truly Personal, Not Generic",
      content: `Unlike traditional counseling, Skill Lantern does not rely on vague suggestions or general aptitude results. Every recommendation is generated based on your actual data — academic history, personal interests, skills, strengths, and goals.`,
    },
    {
      id: "item-2",
      title: "Built with Advanced AI Models",
      content:
        "Unlike traditional counseling, Skill Lantern does not rely on vague suggestions or general aptitude results. Every recommendation is generated based on your actual data — academic history, personal interests, skills, strengths, and goals.",
    },
    {
      id: "item-3",
      title: "Holistic Guidance",
      content:
        "Unlike traditional counseling, Skill Lantern does not rely on vague suggestions or general aptitude results. Every recommendation is generated based on your actual data — academic history, personal interests, skills, strengths, and goals.",
    },
    {
      id: "item-4",
      title: "Designed for Nepalese Students",
      content:
        "Unlike traditional counseling, Skill Lantern does not rely on vague suggestions or general aptitude results. Every recommendation is generated based on your actual data — academic history, personal interests, skills, strengths, and goals.",
    },
    {
      id: "item-5",
      title: "Clear, Transparent, and Easy to Use",
      content:
        "Unlike traditional counseling, Skill Lantern does not rely on vague suggestions or general aptitude results. Every recommendation is generated based on your actual data — academic history, personal interests, skills, strengths, and goals.",
    },
  ];

  return (
    <main className=" flex flex-col items-center justify-center">
      <section
        className="mx-[50px] max-w-[900px] min-h-screen items-center flex flex-col justify-center gap-10"
        id="Hero"
      >
        <h1 className="text-5xl font-light tracking-[-3.2px] leading-[110%] text-center">
          <span className="font-normal">
            <span className="text-[64px]">D</span>iscover Your Perfect Career
            Path —
          </span>{" "}
          Skill Lantern analyze your skills, interests, and academics to
          recommend the best career roadmap tailored just for you.
        </h1>

        <p>
          Start discovering your career today with confidence, clarity, and
          direction.
        </p>

        <div className="space-x-10">
          <Link href="/registration/login" className="underline">
            Get Started
          </Link>
          <Link href="#About" className="underline">
            Learn More
          </Link>
        </div>
      </section>

      <section
        className="mx-[50px] flex flex-col items-center justify-center gap-[100px] py-[50px]"
        id="About"
      >
        <h1 className="text-[205px] font-bold tracking-[-5px] leading-[100%]">
          About Skill Lantern
        </h1>
        <p className="text-4xl max-w-[900px] leading-[130%] tracking-[-2px] text-center font-light">
          Skill Lantern is an intelligent career-recommendation platform
          designed to help students, job seekers, and professionals find the
          right career path. By analyzing your abilities, personality,
          interests, and goals, we provide tailored career suggestions, required
          skills, and step-by-step learning roadmaps.
        </p>

        <div className="grid grid-cols-3 gap-[100px] py-[50px]">
          <div className="space-y-5">
            <h1 className="font-bold">Personalized Career Discovery</h1>
            <p className="text-[#555551]">
              Skill Lantern analyzes your skills, interests, and strengths to
              recommend career paths tailored specifically to you. Instead of
              guessing or following random trends, the platform guides you
              toward careers where you are naturally aligned and likely to
              succeed. This ensures clarity, confidence, and a clear direction
              for your future.
            </p>
          </div>
          <div className="space-y-5">
            <h1 className="font-bold">Data-Driven Insights</h1>
            <p className="text-[#555551]">
              Every recommendation in Skill Lantern is backed by real-world
              industry data. The platform compares your profile with current job
              market trends, skill demands, salary ranges, and growth
              opportunities. This helps you understand not just what career fits
              you—but why it fits you.
            </p>
          </div>
          <div className="row-span-2 ">
            <Image
              src="/career-development.png"
              width={500}
              height={500}
              alt="image1"
              className="w-full h-full rounded-md object-cover "
            />
          </div>

          <div className="row-span-2">
            <Image
              src="/career-sign-post.jpg"
              width={500}
              height={500}
              alt="image2"
              className="w-full h-full rounded-xl object-cover"
            />
          </div>
          <div className="space-y-5">
            <h1 className="font-bold">Skill Gap Identification</h1>
            <p className="text-[#555551]">
              Skill Lantern highlights the skills you already have and the ones
              you need to improve. By identifying these gaps early, the platform
              makes career development more efficient. You learn exactly what to
              work on, preventing wasted time and ensuring consistent progress
              toward your goals.
            </p>
          </div>
          <div className="space-y-5">
            <h1 className="font-bold">Guided Learning Roadmaps</h1>
            <p className="text-[#555551]">
              To help you grow, Skill Lantern provides structured learning paths
              for each recommended career. These roadmaps include courses,
              tools, certifications, and step-by-step instructions. Whether
              you&apos;re a beginner or someone switching fields, the platform
              makes learning smooth, achievable, and focused.
            </p>
          </div>
          <div className="space-y-5">
            <h1 className="font-bold">Built for Students and Professionals</h1>
            <p className="text-[#555551]">
              Skill Lantern is designed for everyone—from students exploring
              possibilities to professionals planning career shifts. Its
              user-friendly interface, AI-powered engine, and expert-curated
              resources ensure that anyone can find clarity in their career
              journey. No matter your starting point, Skill Lantern helps you
              move forward with confidence.
            </p>
          </div>
        </div>
      </section>

      <section
        className="flex flex-col items-center justify-center gap-[100px] py-[50px]"
        id="Why"
      >
        <h1 className="text-[153px] font-bold tracking-[-5px] leading-[100%]">
          Why Choose Skill Lantern
        </h1>
        <p className="text-4xl max-w-[900px] leading-[130%] tracking-[-2px] text-center font-light">
          Students today don&apos;t just need information — they need personalized
          guidance that understands their individual strengths. Skill Lantern
          stands out because it blends smart technology with real educational
          context to deliver meaningful results.
        </p>
        <div className="w-full">
          <div className="w-screen relative left-1/2 right-1/2 -mx-[50vw]">
            <Accordion type="single" collapsible className="w-full">
              {accordionItems.map((item, index) => (
                <AccordionItem
                  key={item.id}
                  value={item.id}
                  className={`border-b border-border py-8 ${
                    index === 0 ? "border-t" : ""
                  }`}
                >
                  <div className="px-[100px]">
                    <AccordionTrigger>
                      <ul className="list-disc">
                        <li className="text-4xl max-w-[900px] leading-[130%] tracking-[-2px] text-center font-light">
                          {item.title}
                        </li>
                      </ul>
                    </AccordionTrigger>
                    <AccordionContent className="w-2/4">
                      <p className="text-[#555551] font-light">
                        {item.content}
                      </p>
                    </AccordionContent>
                  </div>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </div>
      </section>

      <section
        id="Join"
        className="w-full px-[50px] py-40 my-30 gap-[100px] bg-[#121212] text-white flex flex-col items-center justify-center"
      >
        <h1 className="text-[176px] font-bold tracking-[-5px] leading-[100%]">
          Join Skill Lantern Now
        </h1>
        <p className="text-[32px] max-w-[900px] leading-[130%] tracking-[-2px] text-center font-light">
          Your dream career is closer than you think. Whether you&apos;re exploring
          possibilities or preparing for your next step, Skill Lantern gives you
          the clarity, confidence, and direction you need. Start discovering
          your personalized career recommendations, explore detailed roadmaps,
          and take your first step toward a successful future.
        </p>

        <p className="text-xl text-center font-light">Begin your journey today — your future starts here.</p>
        
        <button className="px-5 py-4 bg-[#FB0] text-black rounded-xs flex items-center gap-2">Get Started <FaArrowRight /></button>
      </section>
    </main>
  );
}
