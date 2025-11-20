import React from 'react';
import { useNavigate } from 'react-router-dom';

function ActivityListItem({ activity }) {
  const navigate = useNavigate();
  const handleDetailsClick = () => {
    navigate(`/activities/${activity.id}`);
  }
  return (
    <div className="py-4 border-b border-gray-200 flex items-center justify-between">
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-1">{activity.title}</h3>
        <div className="flex space-x-4 text-sm text-gray-500">
          <span>Thời gian: {activity.date}</span>
          <span>Tại: {activity.location}</span>
        </div>
      </div>

      <button 
        onClick={handleDetailsClick}
        className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
      >
        Chi tiết
      </button>
      
    </div>
  );
}

export default ActivityListItem;