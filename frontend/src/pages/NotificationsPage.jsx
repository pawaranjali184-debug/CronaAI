import { useState, useEffect } from 'react';
import { HiOutlineBell } from 'react-icons/hi';
import api from '../api/axios';
import '../styles/pages.css';

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);

  const fetchNotifications = async () => {
    try {
      const res = await api.get('/activity/notifications');
      setNotifications(res.data);
    } catch { /* ignore */ }
  };

  useEffect(() => { fetchNotifications(); }, []);

  const markRead = async (id) => {
    try {
      await api.post(`/activity/notifications/${id}/read`);
      fetchNotifications();
    } catch { /* ignore */ }
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-header-info">
          <h1>Notifications</h1>
          <p>Stay updated on your progress and important reminders.</p>
        </div>
      </div>

      {notifications.length > 0 ? (
        <div>
          {notifications.map((n) => (
            <div
              key={n.id}
              className={`notification-item ${n.read === 'false' ? 'notification-item-unread' : ''}`}
              onClick={() => n.read === 'false' && markRead(n.id)}
              style={{ cursor: n.read === 'false' ? 'pointer' : 'default' }}
            >
              {n.read === 'false' && <div className="notification-dot" />}
              <div className="notification-content">
                <div className="notification-title">{n.title}</div>
                <div className="notification-text">{n.content}</div>
              </div>
              <span className={`badge ${n.priority === 'high' ? 'badge-error' : 'badge-info'}`}>{n.priority}</span>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <div className="empty-state-icon"><HiOutlineBell /></div>
          <div className="empty-state-title">No notifications</div>
          <div className="empty-state-text">You&apos;re all caught up! New notifications will appear here.</div>
        </div>
      )}
    </div>
  );
}
