import React from 'react';
import { useNavigate } from 'react-router-dom';

const StatusBadge = ({ status }) => {
  const statusStyles = {
    approved: 'bg-green-100 text-green-800',
    applied: 'bg-yellow-100 text-yellow-800', 
    rejected: 'bg-red-100 text-red-800',
    withdrawn: 'bg-gray-200 text-gray-700', 
    attended: 'bg-blue-100 text-blue-800',  
    absent: 'bg-purple-100 text-purple-800',
  };
  const statusTexts = {
    approved: 'Đã duyệt',
    applied: 'Chờ duyệt',
    rejected: 'Bị từ chối',
    withdrawn: 'Đã hủy',
    attended: 'Đã tham gia',
    absent: 'Vắng mặt',
  };
  return (
    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusStyles[status] || 'bg-gray-100'}`}>
      {statusTexts[status] || status}
    </span>
  );
};

function MyActivityListItem({ application, onCancelClick }) {
  const navigate = useNavigate();

  const isHistory = ['attended', 'absent', 'rejected', 'withdrawn'].includes(application.status);
  const isUpcoming = ['applied', 'approved'].includes(application.status);
  const canCancel = application.status === 'applied';

  const handleDetailsClick = () => {
    if (application.event_id) {
      navigate(`/activities/${application.event_id}`);
    } else {
      alert("Lỗi: Không tìm thấy ID của hoạt động.");
    }
  };

  return (
    <div className="py-4 border-b border-gray-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div className="flex-grow">
        <h3 className="text-lg font-semibold text-gray-800 mb-1">{application.event_name}</h3>
        <div className="flex flex-col sm:flex-row sm:space-x-4 text-sm text-gray-500">
          <span>Ngày: {new Date(application.work_date).toLocaleDateString('vi-VN')}</span>
          <span>Thời gian: {application.starts_at.substring(0, 5)} - {application.ends_at.substring(0, 5)}</span>
          <span>Tại: {application.location}</span>
        </div>
      </div>

      <div className="flex items-center space-x-3 flex-shrink-0">
        <StatusBadge status={application.status} />

        {isUpcoming && (
          <>
            <button
              onClick={handleDetailsClick}
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md"
            >
              Chi tiết
            </button>
            <button
              onClick={() => onCancelClick(application)}
              className={`font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200
                ${canCancel
                  ? 'bg-red-500 hover:bg-red-600 text-white'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }
              `}
              disabled={!canCancel}
            >
              Hủy
            </button>
          </>
        )}
        {isHistory && (
          <button
            onClick={handleDetailsClick}
            className="bg-gray-500 hover:bg-gray-600 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md"
          >
            Xem lại
          </button>
        )}
      </div>
    </div>
  );
}

export default MyActivityListItem;