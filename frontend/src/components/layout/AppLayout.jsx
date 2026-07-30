import { useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

const FULL_BLEED_ROUTES = ['/chat'];

export default function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  const isFull = FULL_BLEED_ROUTES.includes(location.pathname);

  return (
    <div className="app-layout">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="app-content-wrapper">
        <Topbar onMenuToggle={() => setSidebarOpen((prev) => !prev)} />
        <main className={`app-content${isFull ? ' app-content-full' : ''}`}>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
