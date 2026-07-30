import { useState } from 'react';
import { HiOutlineUser, HiOutlineLogout } from 'react-icons/hi';
import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import '../styles/pages.css';

export default function ProfilePage() {
  const { user, updateProfile, logout } = useAuth();
  const navigate = useNavigate();
  const [editing, setEditing] = useState(false);
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [loading, setLoading] = useState(false);

  const getInitials = (name) => {
    if (!name) return '?';
    return name.split(' ').map((w) => w[0]).join('').toUpperCase().slice(0, 2);
  };

  const handleSave = async () => {
    if (!fullName.trim()) return;
    setLoading(true);
    try {
      await updateProfile({ full_name: fullName.trim() });
      setEditing(false);
    } catch { /* ignore */ }
    setLoading(false);
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-header-info">
          <h1>Profile</h1>
          <p>Manage your account and personal information.</p>
        </div>
      </div>

      {/* Profile Card */}
      <div className="profile-card">
        <div className="profile-avatar">{getInitials(user?.full_name)}</div>
        <div className="profile-name">{user?.full_name}</div>
        <div className="profile-email">{user?.email}</div>

        <div className="profile-info-grid">
          <div className="profile-info-item">
            <div className="profile-info-label">Status</div>
            <div className="profile-info-value">{user?.is_active ? 'Active' : 'Inactive'}</div>
          </div>
          <div className="profile-info-item">
            <div className="profile-info-label">Verified</div>
            <div className="profile-info-value">{user?.is_verified ? 'Yes' : 'No'}</div>
          </div>
          <div className="profile-info-item">
            <div className="profile-info-label">Member Since</div>
            <div className="profile-info-value">{user?.created_at ? new Date(user.created_at).toLocaleDateString() : '—'}</div>
          </div>
          <div className="profile-info-item">
            <div className="profile-info-label">Role ID</div>
            <div className="profile-info-value">{user?.role_id || '—'}</div>
          </div>
        </div>
      </div>

      {/* Edit Profile */}
      <div className="form-card">
        <h2><HiOutlineUser /> Edit Profile</h2>
        {editing ? (
          <div>
            <div className="input-group" style={{ marginBottom: 'var(--space-5)' }}>
              <label className="input-label">Full Name</label>
              <input className="input" value={fullName} onChange={(e) => setFullName(e.target.value)} />
            </div>
            <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
              <button className="btn btn-primary" onClick={handleSave} disabled={loading}>
                {loading ? <span className="spinner spinner-sm" /> : 'Save Changes'}
              </button>
              <button className="btn btn-ghost" onClick={() => setEditing(false)}>Cancel</button>
            </div>
          </div>
        ) : (
          <button className="btn btn-secondary" onClick={() => { setFullName(user?.full_name || ''); setEditing(true); }}>
            Edit Name
          </button>
        )}
      </div>

      {/* Logout */}
      <div className="form-card" style={{ borderColor: 'var(--error-light)' }}>
        <h2 style={{ color: 'var(--error)' }}><HiOutlineLogout /> Danger Zone</h2>
        <p style={{ marginBottom: 'var(--space-4)', fontSize: 'var(--text-sm)' }}>Log out of your account on this device.</p>
        <button className="btn btn-danger" onClick={handleLogout}>
          <HiOutlineLogout /> Logout
        </button>
      </div>
    </div>
  );
}
