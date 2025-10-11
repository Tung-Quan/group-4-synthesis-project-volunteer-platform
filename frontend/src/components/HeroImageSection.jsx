import React from 'react';

function HeroImageSection() {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <img src="/volunteer.jpg" alt="Volunteer Group" className="w-full h-auto mb-6" />
      <p className="text-xl font-semibold text-gray-800">Kết nối - Tham gia - Trưởng thành</p>
    </div>
  );
}

export default HeroImageSection;