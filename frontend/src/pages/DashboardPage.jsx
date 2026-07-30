import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  HiOutlineLightningBolt,
  HiOutlineHeart,
  HiOutlineEmojiHappy,
  HiOutlineChartBar,
  HiOutlineChatAlt2,
  HiOutlineMap,
  HiOutlineCollection,
  HiOutlinePlusCircle,
} from 'react-icons/hi';
import { useAuth } from '../hooks/useAuth';
import api from '../api/axios';
import '../styles/dashboard.css';

export default function DashboardPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [statsData, setStatsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/activity/dashboard-stats');
        setStatsData(res.data);
      } catch (err) {
        console.error('Failed to fetch dashboard stats:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  const stats = [
    {
      icon: <HiOutlineLightningBolt />,
      value: loading ? '...' : (statsData?.active_missions ?? 0),
      label: 'Active Missions',
      color: 'purple',
    },
    {
      icon: <HiOutlineHeart />,
      value: loading ? '...' : (statsData?.habits_tracked ?? 0),
      label: 'Habits Tracked',
      color: 'cyan',
    },
    {
      icon: <HiOutlineEmojiHappy />,
      value: loading ? '...' : (statsData?.mood_today ?? '—'),
      label: 'Mood Today',
      color: 'green',
    },
    {
      icon: <HiOutlineChartBar />,
      value: loading ? '...' : (statsData?.predictions_count ?? 0),
      label: 'Predictions',
      color: 'yellow',
    },
  ];

  const quickActions = [
    { icon: <HiOutlineChatAlt2 />, label: 'New Chat', path: '/chat' },
    { icon: <HiOutlineMap />, label: 'Generate Roadmap', path: '/roadmap' },
    { icon: <HiOutlinePlusCircle />, label: 'Create Mission', path: '/missions' },
    { icon: <HiOutlineCollection />, label: 'Add Memory', path: '/memory' },
  ];

  return (
    <div>
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Welcome back, {user?.full_name || 'User'}. Here&apos;s your overview.</p>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        {stats.map((s, i) => (
          <div key={i} className="stat-card">
            <div className={`stat-icon stat-icon-${s.color}`}>{s.icon}</div>
            <div className="stat-value">{s.value}</div>
            <div className="stat-label">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="quick-actions-grid">
          {quickActions.map((action, i) => (
            <button key={i} className="quick-action-btn" onClick={() => navigate(action.path)}>
              <span className="quick-action-icon">{action.icon}</span>
              {action.label}
            </button>
          ))}
        </div>
      </div>

      {/* Getting Started */}
      <div className="dashboard-section">
        <div className="card">
          <div className="card-header">
            <span className="card-title">Getting Started</span>
            <span className="badge badge-primary">New</span>
          </div>
          <div className="card-body">
            <p>Start by chatting with CronaAI to build your profile, then generate a career roadmap and daily missions. Your AI mentor will learn from every interaction.</p>
          </div>
          <div className="card-footer">
            <button className="btn btn-primary btn-sm" onClick={() => navigate('/chat')}>
              Start Chatting
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
