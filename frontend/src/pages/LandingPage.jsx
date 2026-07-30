import { useNavigate } from 'react-router-dom';
import {
  HiOutlineChatAlt2,
  HiOutlineMap,
  HiOutlineLightningBolt,
  HiOutlineChartBar,
  HiOutlineCollection,
  HiOutlineHeart,
} from 'react-icons/hi';
import '../styles/landing.css';

const features = [
  {
    icon: <HiOutlineChatAlt2 />,
    title: 'AI Chatbot',
    desc: 'Personalized conversations that remember your goals, context, and progress across every session.',
  },
  {
    icon: <HiOutlineMap />,
    title: 'Career Roadmap',
    desc: 'Structured learning paths with milestones, timelines, and resources tailored to your dream career.',
  },
  {
    icon: <HiOutlineLightningBolt />,
    title: 'Daily Missions',
    desc: 'AI-generated daily tasks that break your long-term roadmap into actionable, achievable steps.',
  },
  {
    icon: <HiOutlineChartBar />,
    title: 'Future Predictions',
    desc: 'Estimate your career outcomes based on current skills, habits, and progress with gap analysis.',
  },
  {
    icon: <HiOutlineCollection />,
    title: 'Future Memory',
    desc: 'Persistent memory that stores important context so AI always remembers who you are.',
  },
  {
    icon: <HiOutlineHeart />,
    title: 'Habit Tracker',
    desc: 'Build consistent habits with tracking, streaks, and mood logging to fuel your growth.',
  },
];

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing">
      {/* Navbar */}
      <nav className="landing-nav">
        <div className="landing-nav-logo">
          <div className="landing-nav-logo-icon">C</div>
          <span className="landing-nav-logo-text">CronaAI</span>
        </div>
        <div className="landing-nav-links">
          <button className="btn btn-ghost" onClick={() => navigate('/login')}>
            Sign In
          </button>
          <button className="btn btn-primary" onClick={() => navigate('/register')}>
            Get Started
          </button>
        </div>
      </nav>

      {/* Hero */}
      <section className="landing-hero">
        <div className="landing-hero-badge">✨ AI-Powered Personal Life Architect</div>
        <h1>
          Build Your Future{' '}
          <span className="text-gradient">Before You Live It</span>
        </h1>
        <p className="landing-hero-subtitle">
          CronaAI understands who you are, where you are, and what you want to become.
          It creates a personalized roadmap, daily missions, and predictions to guide you
          toward your dream future.
        </p>
        <div className="landing-hero-actions">
          <button className="btn btn-primary btn-lg" onClick={() => navigate('/register')}>
            Start Your Journey
          </button>
          <button className="btn btn-secondary btn-lg" onClick={() => navigate('/login')}>
            Sign In
          </button>
        </div>
      </section>

      {/* Features */}
      <section className="landing-features">
        <h2 className="landing-features-title">
          Everything You Need to <span className="text-gradient">Shape Your Future</span>
        </h2>
        <p className="landing-features-subtitle">
          Six powerful AI modules working together as your personal growth engine.
        </p>
        <div className="landing-features-grid">
          {features.map((f, i) => (
            <div key={i} className="landing-feature-card">
              <div className="landing-feature-icon">{f.icon}</div>
              <h3 className="landing-feature-title">{f.title}</h3>
              <p className="landing-feature-desc">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="landing-cta">
        <h2>Ready to Build Your Future?</h2>
        <p>Join CronaAI and let AI guide your personal growth journey.</p>
        <button className="btn btn-primary btn-lg" onClick={() => navigate('/register')}>
          Get Started — It&apos;s Free
        </button>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        © {new Date().getFullYear()} CronaAI. Built with purpose.
      </footer>
    </div>
  );
}
