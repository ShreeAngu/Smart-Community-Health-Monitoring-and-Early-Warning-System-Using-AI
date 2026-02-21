import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';

interface User {
  id: number;
  email: string;
  role: 'community' | 'admin';
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<{ success: boolean; role?: string }>;
  logout: () => void;
  isAuthenticated: boolean;
  isAdmin: boolean;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Check for existing token on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string): Promise<{ success: boolean; role?: string }> => {
    try {
      console.log('Attempting login with:', { email, password: '***' });
      
      const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      console.log('Login response status:', response.status);

      if (response.ok) {
        const data = await response.json();
        console.log('Login response data:', data);
        const accessToken = data.access_token;
        
        if (!accessToken) {
          console.error('No access token in response');
          return { success: false };
        }
        
        // Get user info
        console.log('Fetching user info with token:', accessToken.substring(0, 20) + '...');
        const userResponse = await fetch('http://localhost:8000/auth/me', {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });

        console.log('User response status:', userResponse.status);

        if (userResponse.ok) {
          const userData = await userResponse.json();
          console.log('User data received:', userData);
          
          // Save to state and localStorage
          setToken(accessToken);
          setUser(userData);
          localStorage.setItem('token', accessToken);
          localStorage.setItem('user', JSON.stringify(userData));
          
          console.log('Login successful, user role:', userData.role);
          return { success: true, role: userData.role };
        } else {
          const errorText = await userResponse.text();
          console.error('User info fetch failed:', errorText);
        }
      } else {
        const errorText = await response.text();
        console.error('Login request failed:', errorText);
      }
      return { success: false };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false };
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const value: AuthContextType = {
    user,
    token,
    login,
    logout,
    isAuthenticated: !!token && !!user,
    isAdmin: user?.role === 'admin',
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};