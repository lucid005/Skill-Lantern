"use client";

import { ReactNode, useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

type AnimationType = "fade-up" | "fade-down" | "fade-left" | "fade-right" | "fade" | "scale";

interface GSAPSectionProps {
  children: ReactNode;
  className?: string;
  animation?: AnimationType;
  duration?: number;
  delay?: number;
  ease?: string;
  start?: string;
}

export function GSAPSection({
  children,
  className = "",
  animation = "fade-up",
  duration = 0.8,
  delay = 0,
  ease = "power2.out",
  start = "top 85%",
}: GSAPSectionProps) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    // Initial state
    const initialState: gsap.TweenVars = { opacity: 0 };
    const animateState: gsap.TweenVars = { opacity: 1, duration, delay, ease };

    switch (animation) {
      case "fade-up":
        initialState.y = 40;
        animateState.y = 0;
        break;
      case "fade-down":
        initialState.y = -40;
        animateState.y = 0;
        break;
      case "fade-left":
        initialState.x = -40;
        animateState.x = 0;
        break;
      case "fade-right":
        initialState.x = 40;
        animateState.x = 0;
        break;
      case "scale":
        initialState.scale = 0.95;
        animateState.scale = 1;
        break;
    }

    gsap.set(element, initialState);

    const scrollTrigger = ScrollTrigger.create({
      trigger: element,
      start,
      toggleActions: "play none none none",
      onEnter: () => gsap.to(element, animateState),
    });

    return () => {
      scrollTrigger.kill();
    };
  }, [animation, duration, delay, ease, start]);

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  );
}

// Stagger children animation
interface GSAPStaggerProps {
  children: ReactNode;
  className?: string;
  animation?: AnimationType;
  duration?: number;
  stagger?: number;
  start?: string;
}

export function GSAPStagger({
  children,
  className = "",
  animation = "fade-up",
  duration = 0.6,
  stagger = 0.1,
  start = "top 85%",
}: GSAPStaggerProps) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = ref.current;
    if (!container) return;

    // Use children directly instead of querySelectorAll
    const elements = Array.from(container.children);
    if (elements.length === 0) return;

    const initialState: gsap.TweenVars = { opacity: 0 };
    const animateState: gsap.TweenVars = { opacity: 1, duration, stagger, ease: "power2.out" };

    switch (animation) {
      case "fade-up":
        initialState.y = 30;
        animateState.y = 0;
        break;
      case "fade-down":
        initialState.y = -30;
        animateState.y = 0;
        break;
      case "fade-left":
        initialState.x = -30;
        animateState.x = 0;
        break;
      case "fade-right":
        initialState.x = 30;
        animateState.x = 0;
        break;
      case "scale":
        initialState.scale = 0.9;
        animateState.scale = 1;
        break;
    }

    gsap.set(elements, initialState);

    const scrollTrigger = ScrollTrigger.create({
      trigger: container,
      start,
      toggleActions: "play none none none",
      onEnter: () => gsap.to(elements, animateState),
    });

    return () => {
      scrollTrigger.kill();
    };
  }, [animation, duration, stagger, start]);

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  );
}
