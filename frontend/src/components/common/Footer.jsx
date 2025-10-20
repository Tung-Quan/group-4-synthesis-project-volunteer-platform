import React from 'react';

function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 py-1.5 px-8 text-sm mt-auto">
      <div className="max-w-7xl mx-auto flex justify-between items-start">
        <div className='text-left'>
          <p>Copyright@2025 Trường đại học Bách Khoa Hồ Chí Minh.</p>
          <p className="flex items-center mb-1">
            <span className="mr-1">📞</span> 0987654321
          </p>
          <p className="flex items-center ">
            <span className="mr-1">📍</span> Địa chỉ: 268 Lý Thường Kiệt, phường Diên Hồng, Thành phố Hồ Chí Minh.
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;