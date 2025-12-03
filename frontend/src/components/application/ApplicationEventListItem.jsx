import React from 'react';
import { useNavigate } from 'react-router-dom';

//the API call is '/applications/{event_id}/{slot_id}'
//display application list by grouping them into the events
function ApplicationEventListItem({ event }) {
  const navigate = useNavigate();
  const handleSeeAppPerEvent = () => {
      console.log(`Đang xem hồ sơ đăng ký gửi về hoạt động: ${event.title} (ID: ${event.id}).`);
      navigate(`/organizer/applications/${event.id}`);
    }
  
  const timeFrame = event.slots?.length > 0
      ? `Từ ${new Date(event.slots[0].work_date).toLocaleDateString('vi-VN')} đến ${new Date(event.slots[event.slots.length - 1].work_date).toLocaleDateString('vi-VN')}`
      : "";

  return (
    <div className="py-4 border-b border-gray-200 flex items-center justify-between">
      <div>
        <h3 className="text-base font-semibold text-gray-800 mb-1">{event.title}</h3>
        <div className="flex space-x-4 text-sm text-gray-500">
          <span>Thời gian: {timeFrame}</span>
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