"use client";

import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

// Register ScrollTrigger plugin
if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

export type AnimationType = "fade-up" | "fade-down" | "fade-left" | "fade-right" | "fade" | "scale";

interface UseGSAPScrollOptions {
  animation?: AnimationType;
  duration?: number;
  delay?: number;
  ease?: string;
  start?: string;
  end?: string;
  toggleActions?: string;
  markers?: boolean;
}

export function useGSAPScroll<T extends HTMLElement>(options: UseGSAPScrollOptions = {}) {
  const ref = useRef<T>(null);
  
  const {
    animation = "fade-up",
    duration = 0.8,
    delay = 0,
    ease = "power2.out",
    start = "top 85%",
    end = "top 20%",
    toggleActions = "play reverse play reverse", // onEnter, onLeave, onEnterBack, onLeaveBack
    markers = false,
  } = options;

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    // Set initial state based on animation type
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
      case "fade":
      default:
        break;
    }

    // Set initial state
    gsap.set(element, initialState);

    // Create scroll trigger animation
    const scrollTrigger = ScrollTrigger.create({
      trigger: element,
      start,
      end,
      toggleActions,
      markers,
      onEnter: () => gsap.to(element, animateState),
      onLeave: () => gsap.to(element, { ...initialState, duration: duration * 0.5 }),
      onEnterBack: () => gsap.to(element, animateState),
      onLeaveBack: () => gsap.to(element, { ...initialState, duration: duration * 0.5 }),
    });

    return () => {
      scrollTrigger.kill();
    };
  }, [animation, duration, delay, ease, start, end, toggleActions, markers]);

  return ref;
}

// Stagger animation for lists/grids
export function useGSAPStagger<T extends HTMLElement>(
  selector: string,
  options: UseGSAPScrollOptions & { stagger?: number } = {}
) {
  const containerRef = useRef<T>(null);
  
  const {
    animation = "fade-up",
    duration = 0.6,
    delay = 0,
    ease = "power2.out",
    start = "top 85%",
    toggleActions = "play reverse play reverse",
    stagger = 0.1,
    markers = false,
  } = options;

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const elements = container.querySelectorAll(selector);
    if (elements.length === 0) return;

    // Set initial state based on animation type
    const initialState: gsap.TweenVars = { opacity: 0 };
    const animateState: gsap.TweenVars = { opacity: 1, duration, delay, ease, stagger };

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
      default:
        break;
    }

    // Set initial state for all elements
    gsap.set(elements, initialState);

    // Create scroll trigger
    const scrollTrigger = ScrollTrigger.create({
      trigger: container,
      start,
      toggleActions,
      markers,
      onEnter: () => gsap.to(elements, animateState),
      onLeave: () => gsap.to(elements, { ...initialState, duration: duration * 0.5, stagger: stagger * 0.5 }),
      onEnterBack: () => gsap.to(elements, animateState),
      onLeaveBack: () => gsap.to(elements, { ...initialState, duration: duration * 0.5, stagger: stagger * 0.5 }),
    });

    return () => {
      scrollTrigger.kill();
    };
  }, [selector, animation, duration, delay, ease, start, toggleActions, stagger, markers]);

  return containerRef;
}
