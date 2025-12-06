import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../../api/apiClient';

//Might need to re-add timeframe
function DashboardActivityListItem({ activity }) {
  const navigate = useNavigate();
  const handleDetailsClick = () => {
    navigate(`/organizer/dashboard/${activity.id}`);
  }

  const [error, setError] = useState(null);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  useEffect(() => {
    const fetchTime = async () => {
      try {
        const response = await apiClient.get(`/events/${activity.id}`);
        const workDates = response.data.slots.map(slot => new Date(slot.work_date));
        setStartDate(new Date(Math.min(...workDates)).toLocaleDateString('vi-VN'));
        setEndDate(new Date(Math.max(...workDates)).toLocaleDateString('vi-VN'));
      } catch (err) {
        if (err.response?.status === 404) {
          setStartDate(new Date(0));
          setEndDate(new Date(0));
        } else {
          setError("Không thể tải hoạt động. Vui lòng thử lại.");
        }
        console.error(err);
      }
    };
    fetchTime();
  }, [activity.id]);

  if (error) return <div className="text-center p-4 text-red-500">{error}</div>;

  return (
    <div className="py-4 border-b border-gray-200 flex items-center justify-between">
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-1">{activity.title}</h3>
        <div className="flex space-x-4 text-sm text-gray-500">
          <span>Thời gian: từ {startDate} đến {endDate}</span>
          <span>Tại: {activity.location}</span>
        </div>
      </div>

      <button 
        onClick={handleDetailsClick}
        className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
      >
        Quản lý chi tiết
      </button>
      
    </div>
  );
}

export default DashboardActivityListItem;