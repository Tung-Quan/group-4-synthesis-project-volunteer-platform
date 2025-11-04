import React from 'react';

function WelcomeSection() {
  return (
    <div className="relative w-full h-64 md:h-80 rounded-lg overflow-hidden shadow-lg">
      <img 
        src="/loginpicture.jpg"
        alt="Welcome to Bach Khoa Volunteer Hub"
        className="w-full h-full object-cover"
      />
      <div className="absolute inset-0 bg-black bg-opacity-40"></div> {/* Lớp phủ mờ đen */}
      
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center text-white p-4">
        <h2 className="text-3xl md:text-4xl font-bold uppercase" style={{ textShadow: '2px 2px 4px rgba(0,0,0,0.7)' }}>
          Chào mừng bạn đến với Bach Khoa Volunteer Hub
        </h2>
        <p className="mt-4 text-xl md:text-2xl" style={{ textShadow: '1px 1px 3px rgba(0,0,0,0.7)' }}>
          Hãy bắt đầu bằng việc tìm kiếm một hoạt động
        </p>
      </div>
    </div>
  );
}

export default WelcomeSection;