import { NavLink, useLocation } from 'react-router-dom';
import {
  HiOutlineViewGrid,
  HiOutlineChatAlt2,
  HiOutlineMap,
  HiOutlineLightningBolt,
  HiOutlineChartBar,
  HiOutlineCollection,
  HiOutlineHeart,
  HiOutlineEmojiHappy,
  HiOutlineUser,
  HiOutlineCog,
} from 'react-icons/hi';

const mainNav = [
  { to: '/dashboard', icon: HiOutlineViewGrid, label: 'Dashboard' },
  { to: '/chat', icon: HiOutlineChatAlt2, label: 'AI Chat' },
  { to: '/roadmap', icon: HiOutlineMap, label: 'Roadmap' },
  { to: '/missions', icon: HiOutlineLightningBolt, label: 'Missions' },
  { to: '/predictions', icon: HiOutlineChartBar, label: 'Predictions' },
];

const activityNav = [
  { to: '/memory', icon: HiOutlineCollection, label: 'Memory' },
  { to: '/habits', icon: HiOutlineHeart, label: 'Habits' },
  { to: '/mood', icon: HiOutlineEmojiHappy, label: 'Mood' },
];

const bottomNav = [
  { to: '/profile', icon: HiOutlineUser, label: 'Profile' },
];

export default function Sidebar({ isOpen, onClose }) {
  const location = useLocation();

  return (
    <>
      {isOpen && <div className="sidebar-overlay" onClick={onClose} />}
      <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">C</div>
          <span className="sidebar-brand">CronaAI</span>
        </div>

        <nav className="sidebar-nav">
          <div className="sidebar-section-label">Main</div>
          {mainNav.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={onClose}
              className={`sidebar-link ${location.pathname === item.to ? 'sidebar-link-active' : ''}`}
            >
              <span className="sidebar-link-icon"><item.icon /></span>
              {item.label}
            </NavLink>
          ))}

          <div className="sidebar-section-label">Activity</div>
          {activityNav.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={onClose}
              className={`sidebar-link ${location.pathname === item.to ? 'sidebar-link-active' : ''}`}
            >
              <span className="sidebar-link-icon"><item.icon /></span>
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          {bottomNav.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={onClose}
              className={`sidebar-link ${location.pathname === item.to ? 'sidebar-link-active' : ''}`}
            >
              <span className="sidebar-link-icon"><item.icon /></span>
              {item.label}
            </NavLink>
          ))}
        </div>
      </aside>
    </>
  );
}
