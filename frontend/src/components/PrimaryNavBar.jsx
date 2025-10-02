import React from 'react';

// Nhận currentPage prop
function PrimaryNavbar({ currentPage, navigateTo }) {
  return (
    <nav className="bg-white py-3 px-4 text-gray-700 border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center">
        <span
          className="font-semibold text-lg text-gray-800 flex items-center cursor-pointer hover:text-blue-600 transition-colors duration-200"
          onClick={() => navigateTo('home')} // Cho phép quay về trang chủ
        >
          <span className="mr-2 text-xl">🏠</span> TRANG CHỦ
        </span>
        {currentPage === 'login' && (
          <span className="ml-2 font-semibold text-lg text-gray-600 flex items-center">
            <span className="mx-2 text-xl">»</span> ĐĂNG NHẬP
          </span>
        )}
      </div>
    </nav>
  );
}

export default PrimaryNavbar;