import React from 'react'
import { motion } from 'framer-motion'
import { DatabaseZap } from 'lucide-react'
import { Reveal } from '../components/Motion.jsx'

export default function HeroSlide() {
  return (
    <div className="hero-content">
      <Reveal>
        <span className="hero-badge">
          <DatabaseZap className="h-4 w-4" aria-hidden="true" />
          DBMS Course Project
        </span>
      </Reveal>
      <motion.h1
        className="hero-title"
        initial={{ opacity: 0, y: 36, scale: 0.96 }}
        whileInView={{ opacity: 1, y: 0, scale: 1 }}
        viewport={{ once: false }}
        transition={{ duration: 0.75, ease: [0.22, 1, 0.36, 1] }}
      >
        <span className="gradient-text">PlagLe</span>
      </motion.h1>
      <Reveal delay={0.08}>
        <p className="hero-sub-title">Plagiarism Detection System</p>
        <p className="hero-course">DBMS Course Project Presentation</p>
      </Reveal>
      <Reveal delay={0.16}>
        <div className="hero-tagline">
          "An intelligent full-stack platform that detects textual plagiarism in student
          submissions using NLP-powered similarity analysis and MySQL-backed data management."
        </div>
      </Reveal>
      <Reveal className="hero-meta" delay={0.22}>
        <div className="hero-meta-item">
          <div className="hero-meta-label">Presented By</div>
          <div className="hero-meta-value">Vishal Verma, Vedansh Mathur, Vivek Singh, Vishesh Gupta</div>
        </div>
        <div className="hero-meta-item">
          <div className="hero-meta-label">Course</div>
          <div className="hero-meta-value">Database Management Systems</div>
        </div>
        <div className="hero-meta-item">
          <div className="hero-meta-label">Guide</div>
          <div className="hero-meta-value">Dr Aurobindo Behra</div>
        </div>
        <div className="hero-meta-item">
          <div className="hero-meta-label">Date</div>
          <div className="hero-meta-value">30th april, 2026</div>
        </div>
      </Reveal>
    </div>
  )
}
