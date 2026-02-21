import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const DiagnosticPage: React.FC = () => {
  const { user, isAdmin, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold mb-6 text-gray-900">🔍 Dashboard Diagnostic</h1>
        
        <div className="space-y-6">
          {/* Authentication Status */}
          <div className="border-b pb-4">
            <h2 className="text-xl font-semibold mb-3">Authentication Status</h2>
            <div className="space-y-2">
              <p className="flex items-center space-x-2">
                <span className="font-medium">Authenticated:</span>
                <span className={`px-3 py-1 rounded-full text-sm ${isAuthenticated ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                  {isAuthenticated ? '✓ Yes' : '✗ No'}
                </span>
              </p>
              <p className="flex items-center space-x-2">
                <span className="font-medium">Is Admin:</span>
                <span className={`px-3 py-1 rounded-full text-sm ${isAdmin ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'}`}>
                  {isAdmin ? '✓ Yes (Admin)' : '✗ No (Community)'}
                </span>
              </p>
            </div>
          </div>

          {/* User Information */}
          <div className="border-b pb-4">
            <h2 className="text-xl font-semibold mb-3">User Information</h2>
            {user ? (
              <div className="bg-gray-50 p-4 rounded-lg space-y-2">
                <p><span className="font-medium">Email:</span> {user.email}</p>
                <p><span className="font-medium">Role:</span> <span className="uppercase font-bold">{user.role}</span></p>
                <p><span className="font-medium">User ID:</span> {user.id}</p>
                <p><span className="font-medium">Created:</span> {new Date(user.created_at).toLocaleString()}</p>
              </div>
            ) : (
              <p className="text-gray-500">No user data available</p>
            )}
          </div>

          {/* Expected Dashboard */}
          <div className="border-b pb-4">
            <h2 className="text-xl font-semibold mb-3">Expected Dashboard</h2>
            <div className="bg-blue-50 p-4 rounded-lg">
              {isAdmin ? (
                <div>
                  <p className="text-lg font-bold text-red-600">🛡️ Admin Dashboard</p>
                  <p className="text-sm text-gray-600 mt-2">You should see:</p>
                  <ul className="list-disc list-inside text-sm text-gray-700 mt-2 space-y-1">
                    <li>Red shield icon</li>
                    <li>"Admin Dashboard" title</li>
                    <li>Red "ADMIN" badge</li>
                    <li>Interactive heatmap</li>
                    <li>Rainfall simulation slider</li>
                    <li>Statistics cards (4 cards)</li>
                    <li>Charts (pie, bar, line)</li>
                    <li>Alert management table</li>
                  </ul>
                </div>
              ) : (
                <div>
                  <p className="text-lg font-bold text-blue-600">💧 Community Dashboard</p>
                  <p className="text-sm text-gray-600 mt-2">You should see:</p>
                  <ul className="list-disc list-inside text-sm text-gray-700 mt-2 space-y-1">
                    <li>Blue droplet icon</li>
                    <li>"Community Health Dashboard" title</li>
                    <li>Blue "Community User" badge</li>
                    <li>Risk indicator card</li>
                    <li>Symptom reporting form</li>
                    <li>Health education tips (4 tips)</li>
                    <li>Recent alerts panel</li>
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Navigation Buttons */}
          <div className="space-y-3">
            <h2 className="text-xl font-semibold mb-3">Navigation</h2>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => navigate('/admin-dashboard')}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Go to Admin Dashboard
              </button>
              <button
                onClick={() => navigate('/community-dashboard')}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Go to Community Dashboard
              </button>
              <button
                onClick={logout}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>

          {/* LocalStorage Info */}
          <div className="border-b pb-4">
            <h2 className="text-xl font-semibold mb-3">LocalStorage Data</h2>
            <div className="bg-gray-50 p-4 rounded-lg space-y-2 text-sm">
              <p><span className="font-medium">Token exists:</span> {localStorage.getItem('token') ? '✓ Yes' : '✗ No'}</p>
              <p><span className="font-medium">User data exists:</span> {localStorage.getItem('user') ? '✓ Yes' : '✗ No'}</p>
              {localStorage.getItem('user') && (
                <div className="mt-2">
                  <p className="font-medium">Stored user data:</p>
                  <pre className="bg-white p-2 rounded mt-1 overflow-x-auto text-xs">
                    {JSON.stringify(JSON.parse(localStorage.getItem('user') || '{}'), null, 2)}
                  </pre>
                </div>
              )}
            </div>
          </div>

          {/* Current URL */}
          <div>
            <h2 className="text-xl font-semibold mb-3">Current Location</h2>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="font-mono text-sm">{window.location.href}</p>
            </div>
          </div>

          {/* Troubleshooting Tips */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <h3 className="font-semibold text-yellow-900 mb-2">💡 Troubleshooting Tips</h3>
            <ul className="text-sm text-yellow-800 space-y-1 list-disc list-inside">
              <li>If you see the wrong dashboard, try logging out and back in</li>
              <li>Clear browser cache (Ctrl+Shift+Delete)</li>
              <li>Hard refresh the page (Ctrl+F5)</li>
              <li>Check the URL matches your expected dashboard</li>
              <li>Restart the frontend dev server</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DiagnosticPage;
