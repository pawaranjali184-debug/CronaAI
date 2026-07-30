import { useNavigate } from 'react-router-dom';
import { HiOutlineBell, HiOutlineMenu } from 'react-icons/hi';
import { useAuth } from '../../hooks/useAuth';

export default function Topbar({ onMenuToggle }) {
  const { user } = useAuth();
  const navigate = useNavigate();

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  const getInitials = (name) => {
    if (!name) return '?';
    return name.split(' ').map((w) => w[0]).join('').toUpperCase().slice(0, 2);
  };

  return (
    <header className="topbar">
      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
        <button className="sidebar-mobile-toggle" onClick={onMenuToggle}>
          <HiOutlineMenu />
        </button>
        <div className="topbar-greeting">
          <span className="topbar-greeting-text">{getGreeting()}</span>
          <span className="topbar-greeting-name">{user?.full_name || 'User'}</span>
        </div>
      </div>

      <div className="topbar-actions">
        <button className="topbar-btn" onClick={() => navigate('/notifications')}>
          <HiOutlineBell />
          <span className="topbar-badge" />
        </button>
        <div className="topbar-avatar" onClick={() => navigate('/profile')}>
          {getInitials(user?.full_name)}
        </div>
      </div>
    </header>
  );
}
