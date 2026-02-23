import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const DiagnosticPage: React.FC = () => {
 const { user, isAdmin, isAuthenticated, logout } = useAuth();
 const navigate = useNavigate();

 return (
 <div className="min-h-screen bg-gray-00 p-">
 <div className="max-w-xl mx-auto bg-white rounded-lg shadow-lg p-">
 <h className="text-xl font-bold mb- text-gray-00"> Dashboard Diagnostic</h>

 <div className="space-y-">
 {/* Authentication Status */}
 <div className="border-b pb-">
 <h className="text-xl font-semibold mb-">Authentication Status</h>
 <div className="space-y-">
 <p className="flex items-center space-x-">
 <span className="font-medium">Authenticated:</span>
 <span className={`px- py- rounded-full text-sm ${isAuthenticated ? 'bg-green-00 text-green-00' : 'bg-red-00 text-red-00'}`}>
 {isAuthenticated ? ' Yes' : ' No'}
 </span>
 </p>
 <p className="flex items-center space-x-">
 <span className="font-medium">Is Admin:</span>
 <span className={`px- py- rounded-full text-sm ${isAdmin ? 'bg-red-00 text-red-00' : 'bg-blue-00 text-blue-00'}`}>
 {isAdmin ? ' Yes (Admin)' : ' No (Community)'}
 </span>
 </p>
 </div>
 </div>

 {/* User Information */}
 <div className="border-b pb-">
 <h className="text-xl font-semibold mb-">User Information</h>
 {user ? (
 <div className="bg-gray-0 p- rounded-lg space-y-">
 <p><span className="font-medium">Email:</span> {user.email}</p>
 <p><span className="font-medium">Role:</span> <span className="uppercase font-bold">{user.role}</span></p>
 <p><span className="font-medium">User ID:</span> {user.id}</p>
 <p><span className="font-medium">Created:</span> {new Date(user.created_at).toLocaleString()}</p>
 </div>
 ) : (
 <p className="text-gray-00">No user data available</p>
 )}
 </div>

 {/* Expected Dashboard */}
 <div className="border-b pb-">
 <h className="text-xl font-semibold mb-">Expected Dashboard</h>
 <div className="bg-blue-0 p- rounded-lg">
 {isAdmin ? (
 <div>
 <p className="text-lg font-bold text-red-00"> Admin Dashboard</p>
 <p className="text-sm text-gray-00 mt-">You should see:</p>
 <ul className="list-disc list-inside text-sm text-gray-00 mt- space-y-">
 <li>Red shield icon</li>
 <li>"Admin Dashboard" title</li>
 <li>Red "ADMIN" badge</li>
 <li>Interactive heatmap</li>
 <li>Rainfall simulation slider</li>
 <li>Statistics cards ( cards)</li>
 <li>Charts (pie, bar, line)</li>
 <li>Alert management table</li>
 </ul>
 </div>
 ) : (
 <div>
 <p className="text-lg font-bold text-blue-00"> Community Dashboard</p>
 <p className="text-sm text-gray-00 mt-">You should see:</p>
 <ul className="list-disc list-inside text-sm text-gray-00 mt- space-y-">
 <li>Blue droplet icon</li>
 <li>"Community Health Dashboard" title</li>
 <li>Blue "Community User" badge</li>
 <li>Risk indicator card</li>
 <li>Symptom reporting form</li>
 <li>Health education tips ( tips)</li>
 <li>Recent alerts panel</li>
 </ul>
 </div>
 )}
 </div>
 </div>

 {/* Navigation Buttons */}
 <div className="space-y-">
 <h className="text-xl font-semibold mb-">Navigation</h>
 <div className="flex flex-wrap gap-">
 <button
 onClick={() => navigate('/admin-dashboard')}
 className="px- py- bg-red-00 text-white rounded-lg hover:bg-red-00 transition-colors"
 >
 Go to Admin Dashboard
 </button>
 <button
 onClick={() => navigate('/community-dashboard')}
 className="px- py- bg-blue-00 text-white rounded-lg hover:bg-blue-00 transition-colors"
 >
 Go to Community Dashboard
 </button>
 <button
 onClick={logout}
 className="px- py- bg-gray-00 text-white rounded-lg hover:bg-gray-00 transition-colors"
 >
 Logout
 </button>
 </div>
 </div>

 {/* LocalStorage Info */}
 <div className="border-b pb-">
 <h className="text-xl font-semibold mb-">LocalStorage Data</h>
 <div className="bg-gray-0 p- rounded-lg space-y- text-sm">
 <p><span className="font-medium">Token exists:</span> {localStorage.getItem('token') ? ' Yes' : ' No'}</p>
 <p><span className="font-medium">User data exists:</span> {localStorage.getItem('user') ? ' Yes' : ' No'}</p>
 {localStorage.getItem('user') && (
 <div className="mt-">
 <p className="font-medium">Stored user data:</p>
 <pre className="bg-white p- rounded mt- overflow-x-auto text-xs">
 {JSON.stringify(JSON.parse(localStorage.getItem('user') || '{}'), null, )}
 </pre>
 </div>
 )}
 </div>
 </div>

 {/* Current URL */}
 <div>
 <h className="text-xl font-semibold mb-">Current Location</h>
 <div className="bg-gray-0 p- rounded-lg">
 <p className="font-mono text-sm">{window.location.href}</p>
 </div>
 </div>

 {/* Troubleshooting Tips */}
 <div className="bg-yellow-0 border border-yellow-00 rounded-lg p-">
 <h className="font-semibold text-yellow-00 mb-"> Troubleshooting Tips</h>
 <ul className="text-sm text-yellow-00 space-y- list-disc list-inside">
 <li>If you see the wrong dashboard, try logging out and back in</li>
 <li>Clear browser cache (Ctrl+Shift+Delete)</li>
 <li>Hard refresh the page (Ctrl+F)</li>
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
