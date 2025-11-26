import React from 'react';

const CloverIcon = () => (
  <span className="text-green-500 text-lg mr-2">🍀</span>
);

function ActivityDetailHeader({ activity, onRegisterClick, userType, onCancelClick, applicationStatus }) {
  // Hàm render nút bấm dựa trên các điều kiện
  const renderActionButtons = () => {
    if (userType === 'ORGANIZER') {
      return null;
    }

    if (applicationStatus && applicationStatus.startsWith('completed')) {
      return (
        <div className="bg-gray-200 text-gray-700 font-bold py-2 px-6 rounded-lg cursor-default">
          Đã hoàn thành
        </div>
      );
    }
    
    switch (applicationStatus) {
      case 'pending':
        return (
          <div className="flex space-x-2">
            <div className="bg-yellow-100 text-yellow-800 font-bold py-2 px-6 rounded-lg cursor-default">
              Chờ duyệt
            </div>
            <button
              onClick={onCancelClick}
              className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-6 rounded-lg shadow-md transition-colors duration-200"
            >
              Hủy
            </button>
          </div>
        );
      case 'approved':
        return (
          <div className="flex space-x-2">
            <div className="bg-green-100 text-green-800 font-bold py-2 px-6 rounded-lg cursor-default">
              Đã duyệt
            </div>
            <button
              className="bg-gray-300 text-gray-500 font-bold py-2 px-6 rounded-lg shadow-md cursor-not-allowed"
              disabled
            >
              Hủy
            </button>
          </div>
        );
      case 'rejected':
        return (
          <div className="bg-red-100 text-red-800 font-bold py-2 px-6 rounded-lg cursor-default">
            Bị từ chối
          </div>
        );
      default: // Mặc định là 'null', tức là chưa đăng ký
        return (
          <button 
            onClick={onRegisterClick}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg shadow-md transition-colors duration-200 whitespace-nowrap"
          >
            Đăng ký
          </button>
        );
    }
  };
  
  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">

      <div className="flex items-center justify-between pb-4 border-b border-gray-200">
        <h1 className="text-xl font-bold">
          <span className="text-red-600">{activity.id}</span> - <span className="text-blue-700">{activity.title}</span>
        </h1>
        {renderActionButtons()}
      </div>

      <div className="flex flex-col space-y-2 pt-4">
        {activity.time && (
          <div className="flex items-center">
            <CloverIcon />
            <p className="text-gray-700">
              Thời gian: <span className="text-green-600 font-semibold">{activity.time}</span>
            </p>
          </div>
        )}

        {activity.locationDetail && (
          <div className="flex items-center">
            <CloverIcon />
            <p className="text-gray-700">
              Tại: <span className="text-pink-600 font-semibold">{activity.locationDetail}</span>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ActivityDetailHeader;