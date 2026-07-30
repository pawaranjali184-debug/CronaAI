import { useNavigate } from 'react-router-dom';

export default function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      textAlign: 'center',
      padding: 'var(--space-8)',
      background: 'var(--bg-primary)',
    }}>
      <div style={{
        fontSize: '6rem',
        fontWeight: 'var(--font-extrabold)',
        fontFamily: 'var(--font-heading)',
        background: 'var(--accent-gradient)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
        marginBottom: 'var(--space-4)',
      }}>
        404
      </div>
      <h2 style={{ marginBottom: 'var(--space-2)' }}>Page not found</h2>
      <p style={{ color: 'var(--text-tertiary)', marginBottom: 'var(--space-8)', maxWidth: 400 }}>
        The page you&apos;re looking for doesn&apos;t exist or has been moved.
      </p>
      <button className="btn btn-primary" onClick={() => navigate('/dashboard')}>
        Back to Dashboard
      </button>
    </div>
  );
}
