import React, {useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../../api/apiClient';

//the API call is '/applications/{event_id}/{slot_id}'
//display application list by grouping them into the events
function ApplicationEventListItem({ event }) {
  const navigate = useNavigate();
  const handleSeeAppPerEvent = () => {
      console.log(`Đang xem hồ sơ đăng ký gửi về hoạt động: ${event.title} (ID: ${event.id}).`);
      navigate(`/organizer/applications/${event.id}`);
    }
  
  const [error, setError] = useState(null);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  useEffect(() => {
    const fetchTime = async () => {
      try {
        const response = await apiClient.get(`/events/${event.id}`);
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
  }, [event.id]);

  if (error) return <div className="text-center p-4 text-red-500">{error}</div>;

  return (
    <div className="py-4 border-b border-gray-200 flex items-center justify-between">
      <div>
        <h3 className="text-base font-semibold text-gray-800 mb-1">{event.title}</h3>
        <div className="flex space-x-4 text-sm text-gray-500">
          <span>Thời gian: từ {startDate} đến {endDate}</span>
          <span>Địa điểm: {event.location}</span>
        </div>
      </div>

      <button 
        onClick={handleSeeAppPerEvent}
        className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
      >
        Chi tiết
      </button>
      
    </div>
  );
}

export default ApplicationEventListItem;