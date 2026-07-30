import { useState } from 'react';
import { HiOutlineMap, HiOutlineSparkles } from 'react-icons/hi';
import api from '../api/axios';
import '../styles/pages.css';

export default function RoadmapPage() {
  const [form, setForm] = useState({
    goal_title: '',
    experience_years: '',
    target_role: '',
    skills: '',
    timeline: '',
  });
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!form.goal_title || !form.target_role || !form.timeline) {
      setError('Please fill in goal title, target role, and timeline.');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        goal_title: form.goal_title,
        experience_years: parseInt(form.experience_years) || 0,
        target_role: form.target_role,
        skills: form.skills.split(',').map((s) => s.trim()).filter(Boolean),
        timeline: form.timeline,
      };
      const res = await api.post('/ai/career-roadmaps', payload);
      setResult(res.data);
      setHistory((prev) => [res.data, ...prev]);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate roadmap.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-header-info">
          <h1>Career Roadmap</h1>
          <p>Generate a structured roadmap with milestones, resources, and timelines for your dream career.</p>
        </div>
      </div>

      {/* Form */}
      <div className="form-card">
        <h2><HiOutlineMap /> Generate Roadmap</h2>
        {error && <div className="auth-error" style={{ marginBottom: 'var(--space-4)' }}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="input-group">
              <label className="input-label">Goal Title</label>
              <input className="input" name="goal_title" placeholder="e.g., Become AI Engineer at Google" value={form.goal_title} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label className="input-label">Target Role</label>
              <input className="input" name="target_role" placeholder="e.g., AI Engineer" value={form.target_role} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label className="input-label">Experience (years)</label>
              <input className="input" name="experience_years" type="number" placeholder="e.g., 1" value={form.experience_years} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label className="input-label">Timeline</label>
              <input className="input" name="timeline" placeholder="e.g., 2 years" value={form.timeline} onChange={handleChange} />
            </div>
            <div className="input-group form-grid-full">
              <label className="input-label">Skills (comma-separated)</label>
              <input className="input" name="skills" placeholder="e.g., python, tensorflow, react" value={form.skills} onChange={handleChange} />
            </div>
          </div>
          <div style={{ marginTop: 'var(--space-6)' }}>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <span className="spinner spinner-sm" /> : <><HiOutlineSparkles /> Generate Roadmap</>}
            </button>
          </div>
        </form>
      </div>

      {/* Result */}
      {result && (
        <div className="result-card">
          <h3><HiOutlineMap /> {result.goal_title}</h3>
          <div className="result-field">
            <div className="result-label">Summary</div>
            <div className="result-value">{result.summary}</div>
          </div>
          <div className="result-field">
            <div className="result-label">Timeline</div>
            <div className="result-value">{result.timeline}</div>
          </div>
          <div className="result-field">
            <div className="result-label">Resources</div>
            <div className="result-value">{result.resources}</div>
          </div>
        </div>
      )}

      {/* History */}
      {history.length > 1 && (
        <div>
          <h2 style={{ marginBottom: 'var(--space-4)' }}>Previous Roadmaps</h2>
          <div className="items-grid">
            {history.slice(1).map((r, i) => (
              <div key={i} className="item-card">
                <div className="item-card-header">
                  <span className="item-card-title">{r.goal_title}</span>
                  <span className="badge badge-primary">{r.timeline}</span>
                </div>
                <div className="item-card-body">{r.summary}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
