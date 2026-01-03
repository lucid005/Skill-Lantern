"use client";

import { ReactNode } from "react";
import { motion, Variants } from "framer-motion";

type AnimationType = "fade-up" | "fade-down" | "fade-left" | "fade-right" | "fade" | "scale";

interface MotionSectionProps {
  children: ReactNode;
  className?: string;
  animation?: AnimationType;
  duration?: number;
  delay?: number;
}

const getVariants = (animation: AnimationType): Variants => {
  const baseHidden = { opacity: 0 };
  const baseVisible = { opacity: 1 };

  switch (animation) {
    case "fade-up":
      return {
        hidden: { ...baseHidden, y: 40 },
        visible: { ...baseVisible, y: 0 },
      };
    case "fade-down":
      return {
        hidden: { ...baseHidden, y: -40 },
        visible: { ...baseVisible, y: 0 },
      };
    case "fade-left":
      return {
        hidden: { ...baseHidden, x: -40 },
        visible: { ...baseVisible, x: 0 },
      };
    case "fade-right":
      return {
        hidden: { ...baseHidden, x: 40 },
        visible: { ...baseVisible, x: 0 },
      };
    case "scale":
      return {
        hidden: { ...baseHidden, scale: 0.95 },
        visible: { ...baseVisible, scale: 1 },
      };
    case "fade":
    default:
      return {
        hidden: baseHidden,
        visible: baseVisible,
      };
  }
};

export function MotionSection({
  children,
  className = "",
  animation = "fade-up",
  duration = 0.8,
  delay = 0,
}: MotionSectionProps) {
  const variants = getVariants(animation);

  return (
    <motion.div
      className={className}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.15 }}
      variants={variants}
      transition={{ duration, delay, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}

// Stagger children animation
interface MotionStaggerProps {
  children: ReactNode;
  className?: string;
  animation?: AnimationType;
  duration?: number;
  stagger?: number;
}

export function MotionStagger({
  children,
  className = "",
  animation = "fade-up",
  duration = 0.6,
  stagger = 0.1,
}: MotionStaggerProps) {
  const childVariants = getVariants(animation);

  const containerVariants: Variants = {
    hidden: {},
    visible: {
      transition: {
        staggerChildren: stagger,
      },
    },
  };

  return (
    <motion.div
      className={className}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.15 }}
      variants={containerVariants}
    >
      {Array.isArray(children)
        ? children.map((child, index) => (
            <motion.div
              key={index}
              variants={childVariants}
              transition={{ duration, ease: "easeOut" }}
            >
              {child}
            </motion.div>
          ))
        : children}
    </motion.div>
  );
}
