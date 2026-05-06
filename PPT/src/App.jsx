import React, { useState, useEffect, useCallback, useRef } from 'react'
import HeroSlide from './slides/HeroSlide.jsx'
import OverviewSlide from './slides/OverviewSlide.jsx'
import SchemaSlide from './slides/SchemaSlide.jsx'
import ArchitectureSlide from './slides/ArchitectureSlide.jsx'
import HighlightsSlide from './slides/HighlightsSlide.jsx'

const SLIDE_LABELS = ['Title', 'Overview', 'Schema', 'Architecture', 'Highlights']

export default function App() {
  const [current, setCurrent] = useState(0)
  const containerRef = useRef(null)

  const goTo = useCallback((i) => {
    if (i < 0 || i >= SLIDE_LABELS.length) return
    setCurrent(i)
    containerRef.current?.children[i]?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }, [])

  const next = useCallback(() => goTo(current + 1), [current, goTo])
  const prev = useCallback(() => goTo(current - 1), [current, goTo])

  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
        e.preventDefault()
        next()
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault()
        prev()
      } else if (e.key === 'Home') {
        e.preventDefault()
        goTo(0)
      } else if (e.key === 'End') {
        e.preventDefault()
        goTo(SLIDE_LABELS.length - 1)
      }
    }

    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [next, prev, goTo])

  useEffect(() => {
    const root = containerRef.current
    if (!root) return undefined

    const observer = new IntersectionObserver((entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0]

      if (visible) setCurrent(Number(visible.target.dataset.index))
    }, { root, threshold: [0.52, 0.75] })

    Array.from(root.children).forEach((child) => observer.observe(child))
    return () => observer.disconnect()
  }, [])

  const slides = [
    <HeroSlide key={0} />,
    <OverviewSlide key={1} />,
    <SchemaSlide key={2} />,
    <ArchitectureSlide key={3} />,
    <HighlightsSlide key={4} />,
  ]

  return (
    <div className="relative h-screen overflow-hidden bg-[#0B0F19] text-slate-100">
      <div
        ref={containerRef}
        className="h-screen snap-y snap-mandatory overflow-y-auto overflow-x-hidden scroll-smooth"
      >
        {slides.map((slide, i) => (
          <section
            key={i}
            data-index={i}
            className="slide-shell relative flex min-h-screen snap-start items-center justify-center px-4 py-16 sm:px-6 sm:py-20 lg:px-10"
          >
            <div className="pointer-events-none absolute right-5 top-5 z-10 font-mono text-[0.7rem] tracking-[0.2em] text-slate-500 sm:right-8">
              {String(i + 1).padStart(2, '0')} / {String(SLIDE_LABELS.length).padStart(2, '0')}
            </div>
            <div className="relative z-10 mx-auto w-full max-w-7xl">
              {slide}
            </div>
          </section>
        ))}
      </div>

      <nav className="fixed right-4 top-1/2 z-50 hidden -translate-y-1/2 flex-col gap-3 rounded-full border border-white/10 bg-slate-950/50 p-3 shadow-2xl shadow-indigo-950/40 backdrop-blur-xl lg:flex">
        {SLIDE_LABELS.map((label, i) => (
          <button
            key={i}
            className={`group relative h-3 w-3 rounded-full transition-all duration-300 ${i === current ? 'bg-indigo-400 shadow-[0_0_18px_rgba(99,102,241,0.9)]' : 'bg-slate-600 hover:bg-slate-300'}`}
            onClick={() => goTo(i)}
            aria-label={`Go to ${label}`}
            title={label}
          >
            <span className="pointer-events-none absolute right-6 top-1/2 hidden -translate-y-1/2 whitespace-nowrap rounded-full border border-white/10 bg-slate-950/90 px-3 py-1 text-xs font-medium text-slate-200 shadow-xl group-hover:block">
              {label}
            </span>
          </button>
        ))}
      </nav>

    </div>
  )
}
