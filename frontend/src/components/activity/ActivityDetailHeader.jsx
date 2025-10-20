import React from 'react';

const CloverIcon = () => (
  <span className="text-green-500 text-lg mr-2">🍀</span>
);

function ActivityDetailHeader({ activity, onRegisterClick }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
      
      <div className="flex items-center justify-between pb-4 border-b border-gray-200">
        <h1 className="text-xl font-bold">
          <span className="text-red-600">{activity.id}</span> - <span className="text-blue-700">{activity.title}</span>
        </h1>
        <button 
          onClick={onRegisterClick}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg shadow-md transition-colors duration-200 whitespace-nowrap"
        >
          Đăng ký
        </button>
      </div>

      <div className="flex flex-col space-y-2 pt-4.">
        <div className="flex items-center">
          <CloverIcon />
          <p className="text-gray-700">
            Thời gian: <span className="text-green-600 font-semibold">{activity.time}</span>
          </p>
        </div>
        
        <div className="flex items-center">
          <CloverIcon />
          <p className="text-gray-700">
            Tại: <span className="text-pink-600 font-semibold">{activity.locationDetail}</span>
          </p>
        </div>
      </div>
      
    </div>
  );
}

export default ActivityDetailHeader;