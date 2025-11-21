// src/components/activity/MyActivityListItem.jsx

import React from 'react';

// Component nhỏ để hiển thị trạng thái
const StatusBadge = ({ status }) => {
  const statusStyles = {
    approved: 'bg-green-100 text-green-800',
    pending: 'bg-yellow-100 text-yellow-800',
    rejected: 'bg-red-100 text-red-800',
    'completed-attended': 'bg-blue-100 text-blue-800',
    'completed-absent': 'bg-gray-200 text-gray-800',
  };
  const statusTexts = {
    approved: 'Đã duyệt',
    pending: 'Chờ duyệt',
    rejected: 'Bị từ chối',
    'completed-attended': 'Đã tham gia',
    'completed-absent': 'Vắng',
  };
  return (
    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusStyles[status] || 'bg-gray-100'}`}>
      {statusTexts[status] || 'Không xác định'}
    </span>
  );
};

function MyActivityListItem({ activity, onDetailsClick, onCancelClick }) {
  const isUpcoming = activity.status === 'approved' || activity.status === 'pending';
  const isHistory = activity.status.startsWith('completed');

  const canCancel = activity.status === 'pending';

  return (
    <div className="py-4 border-b border-gray-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      {/* Phần thông tin */}
      <div className="flex-grow">
        <h3 className="text-lg font-semibold text-gray-800 mb-1">{activity.title}</h3>
        <div className="flex flex-col sm:flex-row sm:space-x-4 text-sm text-gray-500">
          <span>Thời gian: {activity.date}</span>
          <span>Tại: {activity.location}</span>
          {/* {isHistory && activity.recordedDays !== undefined && (
            <span className="font-semibold text-green-600">CTXH được ghi nhận: {activity.recordedDays} ngày</span>
          )} */}
        </div>
      </div>

      {/* Phần trạng thái và nút bấm */}
      <div className="flex items-center space-x-3 flex-shrink-0">
        <div className="flex flex-col items-end"> 
          <StatusBadge status={activity.status} />
          {isHistory && activity.recordedDays !== undefined && (
            <span className="text-xs font-semibold text-green-600 mt-1">
              CTXH: {activity.recordedDays} ngày
            </span>
          )}
        </div>
        {isUpcoming && (
          <>
            <button 
              onClick={() => onDetailsClick(activity.id)}
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
            >
              Chi tiết
            </button>
            <button
              onClick={() => canCancel && onCancelClick(activity.id)} 
              // Thay đổi class và thêm thuộc tính 'disabled'
              className={`font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200
                ${canCancel 
                  ? 'bg-red-500 hover:bg-red-600 text-white' 
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }
              `}
              disabled={!canCancel} // Vô hiệu hóa nút nếu không thể hủy
            >
              Hủy
            </button>
          </>
        )}
        {isHistory && (
           <button 
            onClick={() => onDetailsClick(activity.id)}
            className="bg-gray-500 hover:bg-gray-600 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
          >
            Xem lại
          </button>
        )}
      </div>
    </div>
  );
}

export default MyActivityListItem;