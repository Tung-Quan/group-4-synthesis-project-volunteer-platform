import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';

function AttendancePerSlotItem({ slot, index }) {
  const navigate = useNavigate();
  const { activityId } = useParams();
  const handleAttendanceClick = () => {
    navigate(`/organizer/dashboard/${activityId}/${slot.slot_id}/attendance`);
  }
  return (
    <div className="py-4 border-b border-gray-200 flex items-center justify-between">
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-1">Ca {index}</h3>
        <div className="flex space-x-4 text-sm text-gray-500">
          <p>Ngày: {new Date(slot.work_date).toLocaleDateString('vi-VN')}</p>
          <p>Từ: {slot.starts_at} đến: {slot.ends_at}</p>
        </div>
      </div>

      <button 
        onClick={handleAttendanceClick}
        className="bg-green-600 hover:bg-green-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
      >
        Điểm danh
      </button>
      
    </div>
  );
}

export default AttendancePerSlotItem;