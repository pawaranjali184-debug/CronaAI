import { useState } from 'react';
import { HiOutlineEmojiHappy } from 'react-icons/hi';
import api from '../api/axios';
import '../styles/pages.css';

const moods = [
  { emoji: '😊', label: 'Happy', value: 'happy' },
  { emoji: '😌', label: 'Calm', value: 'calm' },
  { emoji: '🔥', label: 'Motivated', value: 'motivated' },
  { emoji: '😐', label: 'Neutral', value: 'neutral' },
  { emoji: '😔', label: 'Sad', value: 'sad' },
  { emoji: '😤', label: 'Frustrated', value: 'frustrated' },
  { emoji: '😴', label: 'Tired', value: 'tired' },
  { emoji: '😰', label: 'Anxious', value: 'anxious' },
];

export default function MoodPage() {
  const [selectedMood, setSelectedMood] = useState('');
  const [intensity, setIntensity] = useState(5);
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedMood) return;

    setLoading(true);
    setSuccess(false);
    try {
      await api.post('/activity/mood', {
        mood: selectedMood,
        intensity,
        notes: notes || null,
      });
      setSuccess(true);
      setSelectedMood('');
      setIntensity(5);
      setNotes('');
    } catch { /* ignore */ }
    setLoading(false);
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-header-info">
          <h1>Mood Log</h1>
          <p>Track your emotional state to understand patterns in your productivity and growth.</p>
        </div>
      </div>

      <div className="form-card">
        <h2><HiOutlineEmojiHappy /> How are you feeling?</h2>

        {success && (
          <div style={{ background: 'var(--success-light)', color: 'var(--success)', padding: 'var(--space-3) var(--space-4)', borderRadius: 'var(--radius-md)', marginBottom: 'var(--space-4)', fontSize: 'var(--text-sm)' }}>
            Mood logged successfully!
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Mood Selector */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 'var(--space-3)', marginBottom: 'var(--space-6)' }}>
            {moods.map((m) => (
              <button
                key={m.value}
                type="button"
                onClick={() => setSelectedMood(m.value)}
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  gap: 'var(--space-2)',
                  padding: 'var(--space-4)',
                  background: selectedMood === m.value ? 'var(--accent-primary-light)' : 'var(--bg-surface)',
                  border: `2px solid ${selectedMood === m.value ? 'var(--accent-primary)' : 'var(--border-primary)'}`,
                  borderRadius: 'var(--radius-xl)',
                  cursor: 'pointer',
                  transition: 'all var(--transition-fast)',
                  fontSize: 'var(--text-sm)',
                  color: 'var(--text-primary)',
                }}
              >
                <span style={{ fontSize: '1.8rem' }}>{m.emoji}</span>
                {m.label}
              </button>
            ))}
          </div>

          {/* Intensity Slider */}
          <div className="input-group" style={{ marginBottom: 'var(--space-5)' }}>
            <label className="input-label">Intensity: {intensity}/10</label>
            <input
              type="range"
              min="1"
              max="10"
              value={intensity}
              onChange={(e) => setIntensity(parseInt(e.target.value))}
              style={{ width: '100%', accentColor: 'var(--accent-primary)' }}
            />
          </div>

          {/* Notes */}
          <div className="input-group" style={{ marginBottom: 'var(--space-6)' }}>
            <label className="input-label">Notes (optional)</label>
            <textarea className="input" placeholder="What's on your mind?" value={notes} onChange={(e) => setNotes(e.target.value)} />
          </div>

          <button type="submit" className="btn btn-primary" disabled={!selectedMood || loading}>
            {loading ? <span className="spinner spinner-sm" /> : 'Log Mood'}
          </button>
        </form>
      </div>
    </div>
  );
}
