import React, { useState } from 'react';

function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault(); 
    console.log('Đăng nhập với:', { username, password });
    
    alert(`Đăng nhập thành công với Username: ${username} (Đây là demo)`);
    
  };

  const handleClear = () => {
    setUsername('');
    setPassword('');
    console.log('Đã xóa dữ liệu form.');
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-xl max-w-md mx-auto my-8">
      <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Đăng nhập</h2>
      <form onSubmit={handleLogin} className="space-y-6">
        <div>
          <label htmlFor="username" className="block text-gray-700 text-sm font-bold mb-2">
            Tên đăng nhập:
          </label>
          <input
            type="text"
            id="username"
            className="shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500"
            placeholder="Nhập tên đăng nhập của bạn"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password" className="block text-gray-700 text-sm font-bold mb-2">
            Mật khẩu:
          </label>
          <input
            type="password"
            id="password"
            className="shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500"
            placeholder="******************"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div className="flex items-center justify-between space-x-4">
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline w-1/2 transition-colors duration-200"
          >
            Đăng nhập
          </button>
          <button
            type="button"
            onClick={handleClear}
            className="bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline w-1/2 transition-colors duration-200"
          >
            Xóa
          </button>
        </div>
      </form>
    </div>
  );
}

export default LoginForm;