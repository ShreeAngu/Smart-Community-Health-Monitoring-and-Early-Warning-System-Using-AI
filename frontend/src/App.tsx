import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';
import Login from './pages/Login';
import CommunityDashboard from './pages/CommunityDashboard';
import AdminDashboard from './pages/AdminDashboard';
import DiagnosticPage from './pages/DiagnosticPage';

function App() {
 return (
 <AuthProvider>
 <Router>
 <div className="App">
 <Routes>
 {/* Public Routes */}
 <Route path="/login" element={<Login />} />

 {/* Diagnostic Route */}
 <Route
 path="/diagnostic"
 element={
 <PrivateRoute>
 <DiagnosticPage />
 </PrivateRoute>
 }
 />

 {/* Protected Routes */}
 <Route
 path="/community-dashboard"
 element={
 <PrivateRoute>
 <CommunityDashboard />
 </PrivateRoute>
 }
 />

 <Route
 path="/admin-dashboard"
 element={
 <PrivateRoute adminOnly>
 <AdminDashboard />
 </PrivateRoute>
 }
 />

 {/* Default redirect */}
 <Route path="/" element={<Navigate to="/login" replace />} />

 {/* Catch all route */}
 <Route path="*" element={<Navigate to="/login" replace />} />
 </Routes>
 </div>
 </Router>
 </AuthProvider>
 );
}

export default App;