import { useState, useEffect } from 'react';
import { HiOutlineHeart, HiOutlinePlus, HiOutlineCheck } from 'react-icons/hi';
import api from '../api/axios';
import '../styles/pages.css';

export default function HabitsPage() {
  const [habits, setHabits] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: '', frequency: '', target: '' });
  const [loading, setLoading] = useState(false);
  const [loggedToday, setLoggedToday] = useState(new Set());
  const [loggingId, setLoggingId] = useState(null);

  const fetchHabits = async () => {
    try {
      const res = await api.get('/activity/habits');
      setHabits(res.data);
    } catch { /* ignore */ }
  };

  useEffect(() => { fetchHabits(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.name) return;
    setLoading(true);
    try {
      await api.post('/activity/habits', {
        name: form.name,
        frequency: form.frequency || null,
        target: form.target || null,
      });
      setForm({ name: '', frequency: '', target: '' });
      setShowForm(false);
      fetchHabits();
    } catch { /* ignore */ }
    setLoading(false);
  };

  const logHabit = async (habitId) => {
    if (loggedToday.has(habitId)) return;
    setLoggingId(habitId);
    try {
      await api.post('/activity/habits/logs', {
        habit_id: habitId,
        date: new Date().toISOString(),
        status: 'completed',
        notes: '',
      });
      setLoggedToday((prev) => new Set([...prev, habitId]));
    } catch (err) {
      console.error('Failed to log habit:', err);
    } finally {
      setLoggingId(null);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-header-info">
          <h1>Habits</h1>
          <p>Build consistent habits to fuel your growth.</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          <HiOutlinePlus /> New Habit
        </button>
      </div>

      {showForm && (
        <div className="form-card">
          <h2>Create Habit</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <div className="input-group">
                <label className="input-label">Habit Name</label>
                <input className="input" placeholder="e.g., Daily Coding" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
              </div>
              <div className="input-group">
                <label className="input-label">Frequency</label>
                <input className="input" placeholder="e.g., daily, weekly" value={form.frequency} onChange={(e) => setForm({ ...form, frequency: e.target.value })} />
              </div>
              <div className="input-group form-grid-full">
                <label className="input-label">Target</label>
                <input className="input" placeholder="e.g., 2 hours" value={form.target} onChange={(e) => setForm({ ...form, target: e.target.value })} />
              </div>
            </div>
            <div style={{ marginTop: 'var(--space-6)', display: 'flex', gap: 'var(--space-3)' }}>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? <span className="spinner spinner-sm" /> : 'Create Habit'}
              </button>
              <button type="button" className="btn btn-ghost" onClick={() => setShowForm(false)}>Cancel</button>
            </div>
          </form>
        </div>
      )}

      {habits.length > 0 ? (
        <div className="items-grid">
          {habits.map((h) => {
            const isLogged = loggedToday.has(h.id);
            const isLogging = loggingId === h.id;
            return (
              <div key={h.id} className="item-card">
                <div className="item-card-header">
                  <span className="item-card-title">{h.name}</span>
                  <span className={`badge ${h.status === 'active' ? 'badge-success' : 'badge-warning'}`}>{h.status}</span>
                </div>
                <div className="item-card-body">
                  {h.frequency && <span>Frequency: {h.frequency}</span>}
                  {h.target && <span> · Target: {h.target}</span>}
                </div>
                <div className="item-card-footer">
                  <span className="item-card-meta">Created {new Date(h.created_at).toLocaleDateString()}</span>
                  <button
                    className={`btn btn-sm ${isLogged ? 'btn-success' : 'btn-secondary'}`}
                    onClick={() => logHabit(h.id)}
                    disabled={isLogged || isLogging}
                    style={isLogged ? { opacity: 0.85, cursor: 'default' } : {}}
                  >
                    {isLogging ? (
                      <span className="spinner spinner-sm" />
                    ) : isLogged ? (
                      <><HiOutlineCheck /> Logged ✓</>
                    ) : (
                      <><HiOutlineCheck /> Log Today</>
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="empty-state">
          <div className="empty-state-icon"><HiOutlineHeart /></div>
          <div className="empty-state-title">No habits yet</div>
          <div className="empty-state-text">Create your first habit to start building consistency.</div>
        </div>
      )}
    </div>
  );
}
