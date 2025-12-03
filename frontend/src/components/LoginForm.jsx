import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; 
import apiClient from '../api/apiClient';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null); 
  const [isLoading, setIsLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const response = await apiClient.post('/auth/login', {
        email: email,
        password: password,
      });

      const { user, csrf_token } = response.data;
      login(user, csrf_token);

      const fromPath = location.state?.from?.pathname;
      if (fromPath && fromPath !== '/login' && fromPath !== '/guest') {
        navigate(fromPath, { replace: true });
      } else {
        navigate('/', { replace: true });
      }

    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Email hoặc mật khẩu không đúng.';
      setError(errorMessage);
      console.error("Login failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setEmail('');
    setPassword('');
  };

  return (
    <div className="bg-white p-6 border-2 border-gray-400 rounded-lg shadow-lg w-full max-w-md">
      <h2 className="text-2xl font-bold text-center text-red-600 mb-6">Đăng nhập</h2>
      
      <form onSubmit={handleLogin} className="space-y-4">
        <div className="space-y-2">
          <label htmlFor="email" className="block text-gray-700 font-semibold">
            Email
          </label>
          <input
            type="email"
            id="email"
            className="w-full py-2 px-3 bg-gray-200 border border-gray-400 rounded-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="Nhập email của bạn"
          />
        </div>

        <div className="space-y-2">
          <label htmlFor="password" className="block text-gray-700 font-semibold">
            Mật khẩu
          </label>
          <input
            type="password"
            id="password"
            className="w-full py-2 px-3 bg-gray-200 border border-gray-400 rounded-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        
        {error && (
          <div className="text-red-600 text-sm text-center p-2 bg-red-100 rounded">
            {error}
          </div>
        )}

        <div className="flex items-center justify-start space-x-4 pt-2">
          <button
            type="submit"
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-md shadow-md transition-colors duration-200 disabled:bg-blue-300 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Đang xử lý...' : 'Đăng nhập'}
          </button>
          <button
            type="button"
            onClick={handleClear}
            className="bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-6 rounded-md shadow-md transition-colors duration-200"
          >
            Xóa
          </button>
        </div>
      </form>
    </div>
  );
}

export default LoginForm;