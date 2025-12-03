import { useState } from "react";
import { useParams } from "react-router-dom";
import apiClient from "../../api/apiClient";
import ApplicationReviewModal from "./ApplicationReviewModal";

function ApplicationListItem({ application }) {
	const { activityId, slotId } = useParams();

	const [isEditModalOpen, setIsEditModalOpen] = useState(false);
	const [approved, setApproved] = useState(false);

 	const handleAccept = async (updatedData) => {
		try {
            const response = await apiClient.patch(`/applications/${activityId}/review`, updatedData);
            alert(`Đã duyệt ${application.student_name} - ${application.student_no}.`);
            setIsEditModalOpen(false);
        } catch (err) {
            console.error("Sending review failed:", err);
            alert(`Lỗi: ${err.response?.data?.detail || 'Không thể cập nhật trạng thái hồ sơ.'}`);
        }
    };

	const handleReject = async (updatedData) => {
		try {
            const response = await apiClient.patch(`/applications/${activityId}/review`, updatedData);
            console.log(`Đã từ chối ${application.student_name} - ${application.student_no}.`);
            setIsEditModalOpen(false);
        } catch (err) {
            console.error("Sending review failed:", err);
            alert(`Lỗi: ${err.response?.data?.detail || 'Không thể cập nhật trạng thái hồ sơ.'}`);
        }
	};

  return (
    <div className="py-4 border-b border-gray-200 flex items-center justify-between">
      <div>
        <h3 className="text-base font-semibold text-gray-800 mb-1">{application.student_name} - {application.student_no}</h3>
        <div className="flex space-x-4 text-sm text-gray-500">
          <span>Nội dung gửi đăng kí: {application.note}</span>
        </div>
      </div>

      <div className="flex items-center space-x-2 flex-shrink-0 ">
        <button 
          onClick={() => {setIsEditModalOpen(true); setApproved(true)}}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
        >
          Đồng ý
        </button>
        <button 
          onClick={() => {setIsEditModalOpen(true); setApproved(false)}}
          className="bg-red-500 hover:bg-red-600 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
        >
          Từ chối
        </button>
      </div>
      
      
	  <ApplicationReviewModal
		isOpen={isEditModalOpen}
		onClose={() => setIsEditModalOpen(false)}
		slotId={slotId}
		student_user_id={application.student_user_id}
		approved={approved}
		onSave={approved ? handleAccept : handleReject}
	  />
    </div>
  );
}

export default ApplicationListItem;