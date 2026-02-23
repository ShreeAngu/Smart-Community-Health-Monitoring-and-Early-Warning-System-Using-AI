import React, { useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Droplets, AlertCircle } from 'lucide-react';

const Login: React.FC = () => {
 const [email, setEmail] = useState('');
 const [password, setPassword] = useState('');
 const [error, setError] = useState('');
 const [loading, setLoading] = useState(false);
 const [redirectPath, setRedirectPath] = useState<string | null>(null);

 const { login, isAuthenticated, isAdmin } = useAuth();
 const location = useLocation();

 // Handle redirect after state updates
 if (redirectPath) {
 return <Navigate to={redirectPath} replace />;
 }

 // Redirect if already authenticated (from page refresh or direct navigation)
 if (isAuthenticated) {
 const from = location.state?.from?.pathname || (isAdmin ? '/admin-dashboard' : '/community-dashboard');
 return <Navigate to={from} replace />;
 }

 const handleSubmit = async (e: React.FormEvent) => {
 e.preventDefault();
 setError('');
 setLoading(true);

 try {
 const result = await login(email, password);
 if (result.success && result.role) {
 // Set redirect path based on role
 const path = result.role === 'admin' ? '/admin-dashboard' : '/community-dashboard';
 console.log('Login successful, setting redirect to:', path);
 setRedirectPath(path);
 } else {
 setError('Invalid email or password');
 setLoading(false);
 }
 } catch (err) {
 setError('Login failed. Please try again.');
 setLoading(false);
 }
 };

 return (
 <div className="min-h-screen bg-gradient-to-br from-blue-0 to-indigo-00 flex items-center justify-center py- px- sm:px- lg:px-">
 <div className="max-w-md w-full space-y-">
 <div>
 <div className="mx-auto h- w- flex items-center justify-center rounded-full bg-blue-00">
 <Droplets className="h- w- text-blue-00" />
 </div>
 <h className="mt- text-center text-xl font-extrabold text-gray-00">
 Water Disease Prediction
 </h>
 <p className="mt- text-center text-sm text-gray-00">
 Sign in to your account
 </p>
 </div>

 <form className="mt- space-y-" onSubmit={handleSubmit}>
 <div className="rounded-md shadow-sm -space-y-px">
 <div>
 <label htmlFor="email" className="sr-only">
 Email address
 </label>
 <input
 id="email"
 name="email"
 type="email"
 autoComplete="email"
 required
 className="appearance-none rounded-none relative block w-full px- py- border border-gray-00 placeholder-gray-00 text-gray-00 rounded-t-md focus:outline-none focus:ring-blue-00 focus:border-blue-00 focus:z-0 sm:text-sm"
 placeholder="Email address"
 value={email}
 onChange={(e) => setEmail(e.target.value)}
 />
 </div>
 <div>
 <label htmlFor="password" className="sr-only">
 Password
 </label>
 <input
 id="password"
 name="password"
 type="password"
 autoComplete="current-password"
 required
 className="appearance-none rounded-none relative block w-full px- py- border border-gray-00 placeholder-gray-00 text-gray-00 rounded-b-md focus:outline-none focus:ring-blue-00 focus:border-blue-00 focus:z-0 sm:text-sm"
 placeholder="Password"
 value={password}
 onChange={(e) => setPassword(e.target.value)}
 />
 </div>
 </div>

 {error && (
 <div className="flex items-center space-x- text-red-00 text-sm">
 <AlertCircle className="h- w-" />
 <span>{error}</span>
 </div>
 )}

 <div>
 <button
 type="submit"
 disabled={loading}
 className="group relative w-full flex justify-center py- px- border border-transparent text-sm font-medium rounded-md text-white bg-blue-00 hover:bg-blue-00 focus:outline-none focus:ring- focus:ring-offset- focus:ring-blue-00 disabled:opacity-0 disabled:cursor-not-allowed"
 >
 {loading ? (
 <div className="animate-spin rounded-full h- w- border-b- border-white"></div>
 ) : (
 'Sign in'
 )}
 </button>
 </div>

 <div className="text-center">
 <p className="text-sm text-gray-00 mb-">
 Demo Credentials:
 </p>
 <div className="space-y- text-xs text-gray-00">
 <div className="bg-blue-0 p- rounded">
 <p className="font-medium text-blue-00"> Admin User:</p>
 <p>Email: admin@example.com</p>
 <p>Password: admin</p>
 </div>
 <div className="bg-green-0 p- rounded">
 <p className="font-medium text-green-00"> Community User:</p>
 <p>Email: community@example.com</p>
 <p>Password: community</p>
 </div>
 </div>
 </div>
 </form>
 </div>
 </div>
 );
};

export default Login;