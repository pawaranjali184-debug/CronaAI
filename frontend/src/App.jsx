import { Routes, Route } from 'react-router-dom';
import ProtectedRoute from './components/auth/ProtectedRoute';
import AppLayout from './components/layout/AppLayout';

// Public pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

// Protected pages
import DashboardPage from './pages/DashboardPage';
import ChatPage from './pages/ChatPage';
import RoadmapPage from './pages/RoadmapPage';
import MissionsPage from './pages/MissionsPage';
import PredictionsPage from './pages/PredictionsPage';
import MemoryPage from './pages/MemoryPage';
import HabitsPage from './pages/HabitsPage';
import MoodPage from './pages/MoodPage';
import ProfilePage from './pages/ProfilePage';
import NotificationsPage from './pages/NotificationsPage';
import NotFoundPage from './pages/NotFoundPage';

export default function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Protected routes with app layout */}
      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/roadmap" element={<RoadmapPage />} />
        <Route path="/missions" element={<MissionsPage />} />
        <Route path="/predictions" element={<PredictionsPage />} />
        <Route path="/memory" element={<MemoryPage />} />
        <Route path="/habits" element={<HabitsPage />} />
        <Route path="/mood" element={<MoodPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/notifications" element={<NotificationsPage />} />
      </Route>

      {/* 404 */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
