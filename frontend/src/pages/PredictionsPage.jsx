import { useState } from 'react';
import { HiOutlineChartBar, HiOutlineSparkles } from 'react-icons/hi';
import api from '../api/axios';
import '../styles/pages.css';

export default function PredictionsPage() {
  const [form, setForm] = useState({
    age: '',
    education: '',
    skills: '',
    habits: '',
    goals: '',
    personality: '',
    daily_routine: '',
    interests: '',
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!form.age || !form.education || !form.skills) {
      setError('Please fill in at least age, education, and skills.');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        age: parseInt(form.age),
        education: form.education,
        skills: form.skills.split(',').map((s) => s.trim()).filter(Boolean),
        habits: form.habits.split(',').map((s) => s.trim()).filter(Boolean),
        goals: form.goals.split(',').map((s) => s.trim()).filter(Boolean),
        personality: form.personality || 'analytical',
        daily_routine: form.daily_routine || 'standard',
        interests: form.interests.split(',').map((s) => s.trim()).filter(Boolean),
      };
      const res = await api.post('/ai/future-predictions', payload);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-header-info">
          <h1>Future Predictions</h1>
          <p>Estimate your career outcomes based on current skills, habits, and progress.</p>
        </div>
      </div>

      {/* Form */}
      <div className="form-card">
        <h2><HiOutlineChartBar /> Generate Prediction</h2>
        {error && <div className="auth-error" style={{ marginBottom: 'var(--space-4)' }}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="input-group">
              <label className="input-label">Age</label>
              <input className="input" name="age" type="number" placeholder="e.g., 22" value={form.age} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label className="input-label">Education</label>
              <input className="input" name="education" placeholder="e.g., B.Tech in CS" value={form.education} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label className="input-label">Skills (comma-separated)</label>
              <input className="input" name="skills" placeholder="e.g., python, react, ML" value={form.skills} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label className="input-label">Habits (comma-separated)</label>
              <input className="input" name="habits" placeholder="e.g., reading, coding daily" value={form.habits} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label className="input-label">Goals (comma-separated)</label>
              <input className="input" name="goals" placeholder="e.g., become AI engineer" value={form.goals} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label className="input-label">Personality</label>
              <input className="input" name="personality" placeholder="e.g., analytical, creative" value={form.personality} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label className="input-label">Daily Routine</label>
              <input className="input" name="daily_routine" placeholder="e.g., study 4hrs, code 3hrs" value={form.daily_routine} onChange={handleChange} />
            </div>
            <div className="input-group">
              <label className="input-label">Interests (comma-separated)</label>
              <input className="input" name="interests" placeholder="e.g., AI, startups" value={form.interests} onChange={handleChange} />
            </div>
          </div>
          <div style={{ marginTop: 'var(--space-6)' }}>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <span className="spinner spinner-sm" /> : <><HiOutlineSparkles /> Generate Prediction</>}
            </button>
          </div>
        </form>
      </div>

      {/* Result */}
      {result && (
        <div className="result-card">
          <h3><HiOutlineChartBar /> Your Prediction</h3>

          {result.success_probability != null && (
            <div className="probability-display">
              <div className="probability-value">{Math.round(result.success_probability * 100)}%</div>
              <div className="probability-label">Success Probability</div>
            </div>
          )}

          <div className="result-field">
            <div className="result-label">Career Prediction</div>
            <div className="result-value">{result.career_prediction}</div>
          </div>
          <div className="result-field">
            <div className="result-label">Salary Estimate</div>
            <div className="result-value">{result.salary_estimate || '—'}</div>
          </div>
          <div className="result-field">
            <div className="result-label">Recommendations</div>
            <div className="result-value">{result.recommendations || '—'}</div>
          </div>
        </div>
      )}
    </div>
  );
}
