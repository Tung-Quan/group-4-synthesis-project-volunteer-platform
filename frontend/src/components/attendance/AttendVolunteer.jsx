import { useState } from "react";
import { useParams } from "react-router-dom";
import apiClient from "../../api/apiClient";

function AttendVolunteer({ volunteer }) {
	const { activityId, slotId } = useParams();

 	const handleAttendance = async (attend) => {
    try {
      const markAttendance = {
        slot_id: slotId,
        student_user_id: volunteer.student_user_id,
        attended: attend
      }

      const response = await apiClient.patch(`/applications/${activityId}/attendance`, markAttendance);
      alert(`${volunteer.student_name} - ${volunteer.student_no} ${attend ? 'có mặt' : 'vắng'}.`);
    } catch (err) {
      console.error("Taking attendance failed:", err);
      alert(`Lỗi: ${err.response?.data?.detail || 'Không thể gửi yêu cầu điểm danh.'}`);
    }
  };

  return (
    <div className="py-4 border-b border-gray-200 flex items-center justify-between">
      <div>
        <h3 className="text-base font-semibold text-gray-800 mb-1">{volunteer.student_name}</h3>
        <div className="flex space-x-4 text-sm text-gray-700">
          <span>MSSV: {volunteer.student_no}</span>
        </div>
      </div>

      {/* the buttons are sticking together but that'll do for now */}
      <div className="flex items-right">
      <button 
        onClick={() => handleAttendance(true)}
        className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
      >
        Có mặt
      </button>
	    <button 
        onClick={() => {handleAttendance(false)}}
        className="bg-red-500 hover:bg-red-600 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
      >
        Vắng
      </button>
      </div>
    </div>
  );
}

export default AttendVolunteer;