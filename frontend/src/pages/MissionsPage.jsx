import { useState, useEffect } from 'react';
import { HiOutlineLightningBolt, HiOutlineSparkles } from 'react-icons/hi';
import api from '../api/axios';
import '../styles/pages.css';

export default function MissionsPage() {
  const [missionType, setMissionType] = useState('');
  const [preferences, setPreferences] = useState('');
  const [missions, setMissions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch existing missions from DB on mount
  useEffect(() => {
    const fetchMissions = async () => {
      try {
        const res = await api.get('/ai/daily-missions');
        setMissions(res.data);
      } catch (err) {
        console.error('Failed to fetch missions:', err);
      }
    };
    fetchMissions();
  }, []);

  const handleGenerate = async (e) => {
    e.preventDefault();
    setError('');
    if (!missionType) {
      setError('Please enter a mission type.');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        mission_type: missionType,
        preferences: preferences.split(',').map((s) => s.trim()).filter(Boolean),
      };
      const res = await api.post('/ai/daily-missions', payload);
      setMissions((prev) => [res.data, ...prev]);
      setMissionType('');
      setPreferences('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create mission.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-header-info">
          <h1>Daily Missions</h1>
          <p>AI-generated daily tasks that break your goals into actionable steps.</p>
        </div>
      </div>

      {/* Form */}
      <div className="form-card">
        <h2><HiOutlineLightningBolt /> Create Mission</h2>
        {error && <div className="auth-error" style={{ marginBottom: 'var(--space-4)' }}>{error}</div>}
        <form onSubmit={handleGenerate}>
          <div className="form-grid">
            <div className="input-group">
              <label className="input-label">Mission Type</label>
              <input className="input" placeholder="e.g., learning, coding, reading" value={missionType} onChange={(e) => setMissionType(e.target.value)} />
            </div>
            <div className="input-group">
              <label className="input-label">Preferences (comma-separated)</label>
              <input className="input" placeholder="e.g., python, machine learning" value={preferences} onChange={(e) => setPreferences(e.target.value)} />
            </div>
          </div>
          <div style={{ marginTop: 'var(--space-6)' }}>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <span className="spinner spinner-sm" /> : <><HiOutlineSparkles /> Generate Mission</>}
            </button>
          </div>
        </form>
      </div>

      {/* Missions List */}
      {missions.length > 0 && (
        <div className="items-grid">
          {missions.map((m, i) => (
            <div key={m.id || i} className="item-card">
              <div className="item-card-header">
                <span className="item-card-title">{m.title}</span>
                <span className={`badge ${m.status === 'pending' ? 'badge-warning' : 'badge-success'}`}>
                  {m.status}
                </span>
              </div>
              <div className="item-card-body">{m.description}</div>
              <div className="item-card-footer">
                <span className="item-card-meta">{m.mission_type}</span>
                {m.created_at && (
                  <span className="item-card-meta">
                    {new Date(m.created_at).toLocaleDateString()}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {missions.length === 0 && (
        <div className="empty-state">
          <div className="empty-state-icon"><HiOutlineLightningBolt /></div>
          <div className="empty-state-title">No missions yet</div>
          <div className="empty-state-text">Generate your first daily mission above to start building momentum.</div>
        </div>
      )}
    </div>
  );
}
