import React from 'react';

// Nhận onLoginClick và hideLoginButton props
function Header({ onLoginClick, hideLoginButton }) {
  return (
    <header className="relative bg-blue-700 text-white px-4 py-2 h-14 flex items-center justify-end shadow-lg">
      
      <div className="absolute left-1/2 transform -translate-x-1/2 flex items-center">
        <img src="/icon.svg" alt="Bach Khoa Logo" className="h-8 w-auto mr-2" />
        <h1 className="text-xl font-bold whitespace-nowrap">Bach Khoa Volunteer Hub</h1>
      </div>

      
      {!hideLoginButton && (
        <button
          onClick={() => onLoginClick('login')} // Gọi onLoginClick khi bấm
          className="bg-white hover:bg-gray-300 text-black font-semibold py-1.5 px-4 rounded-lg flex items-center transition-colors duration-200 z-10"
        >
          <span className="mr-2 text-lg">👤</span> Đăng nhập
        </button>
      )}
    </header>
  );
}

export default Header;