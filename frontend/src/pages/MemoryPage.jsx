import { useState, useEffect } from 'react';
import { HiOutlineCollection, HiOutlinePlus, HiOutlineSearch, HiOutlineTrash, HiOutlinePencil } from 'react-icons/hi';
import api from '../api/axios';
import '../styles/pages.css';

export default function MemoryPage() {
  const [memories, setMemories] = useState([]);
  const [search, setSearch] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({ title: '', content: '', tags: '' });
  const [loading, setLoading] = useState(false);

  const fetchMemories = async (query = '') => {
    try {
      const url = query ? `/activity/memories?query=${encodeURIComponent(query)}` : '/activity/memories';
      const res = await api.get(url);
      setMemories(res.data);
    } catch { /* ignore */ }
  };

  useEffect(() => {
    fetchMemories();
  }, []);

  const handleSearch = (e) => {
    const val = e.target.value;
    setSearch(val);
    fetchMemories(val);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.title || !form.content) return;

    setLoading(true);
    try {
      const payload = {
        title: form.title,
        content: form.content,
        tags: form.tags.split(',').map((t) => t.trim()).filter(Boolean),
      };

      if (editingId) {
        await api.put(`/activity/memories/${editingId}`, payload);
      } else {
        await api.post('/activity/memories', payload);
      }

      setForm({ title: '', content: '', tags: '' });
      setShowForm(false);
      setEditingId(null);
      fetchMemories(search);
    } catch { /* ignore */ }
    setLoading(false);
  };

  const handleEdit = (m) => {
    setForm({ title: m.title, content: m.content, tags: m.tags || '' });
    setEditingId(m.id);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/activity/memories/${id}`);
      fetchMemories(search);
    } catch { /* ignore */ }
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-header-info">
          <h1>Future Memory</h1>
          <p>Store important context so AI always remembers who you are across sessions.</p>
        </div>
        <button className="btn btn-primary" onClick={() => { setShowForm(!showForm); setEditingId(null); setForm({ title: '', content: '', tags: '' }); }}>
          <HiOutlinePlus /> Add Memory
        </button>
      </div>

      {/* Search */}
      <div className="input-group" style={{ marginBottom: 'var(--space-6)', position: 'relative' }}>
        <HiOutlineSearch style={{ position: 'absolute', left: 14, top: 12, color: 'var(--text-muted)', fontSize: '1.1rem' }} />
        <input className="input" style={{ paddingLeft: '2.5rem' }} placeholder="Search memories..." value={search} onChange={handleSearch} />
      </div>

      {/* Form */}
      {showForm && (
        <div className="form-card">
          <h2>{editingId ? 'Edit Memory' : 'New Memory'}</h2>
          <form onSubmit={handleSubmit}>
            <div className="input-group" style={{ marginBottom: 'var(--space-4)' }}>
              <label className="input-label">Title</label>
              <input className="input" placeholder="e.g., My GATE preparation goal" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
            </div>
            <div className="input-group" style={{ marginBottom: 'var(--space-4)' }}>
              <label className="input-label">Content</label>
              <textarea className="input" placeholder="What should CronaAI remember about you?" value={form.content} onChange={(e) => setForm({ ...form, content: e.target.value })} />
            </div>
            <div className="input-group" style={{ marginBottom: 'var(--space-4)' }}>
              <label className="input-label">Tags (comma-separated)</label>
              <input className="input" placeholder="e.g., python, career, goals" value={form.tags} onChange={(e) => setForm({ ...form, tags: e.target.value })} />
            </div>
            <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? <span className="spinner spinner-sm" /> : (editingId ? 'Update' : 'Save Memory')}
              </button>
              <button type="button" className="btn btn-ghost" onClick={() => { setShowForm(false); setEditingId(null); }}>Cancel</button>
            </div>
          </form>
        </div>
      )}

      {/* Memories Grid */}
      {memories.length > 0 ? (
        <div className="items-grid">
          {memories.map((m) => (
            <div key={m.id} className="item-card">
              <div className="item-card-header">
                <span className="item-card-title">{m.title}</span>
                <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
                  <button className="btn btn-ghost btn-sm" onClick={() => handleEdit(m)}><HiOutlinePencil /></button>
                  <button className="btn btn-ghost btn-sm" onClick={() => handleDelete(m.id)}><HiOutlineTrash /></button>
                </div>
              </div>
              <div className="item-card-body">{m.content}</div>
              {m.tags && (
                <div className="tags">
                  {m.tags.split(',').map((t, i) => <span key={i} className="tag">{t.trim()}</span>)}
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <div className="empty-state-icon"><HiOutlineCollection /></div>
          <div className="empty-state-title">No memories yet</div>
          <div className="empty-state-text">Add your first memory so CronaAI can remember important context about you.</div>
        </div>
      )}
    </div>
  );
}
