import React from 'react';

const CloverIcon = () => (
  <span className="text-green-500 text-lg mr-2">🍀</span>
);

function ActivityDetailHeader({ activity, onRegisterClick, userType, onCancelClick, applicationStatus }) {
  const renderActionButtons = () => {
    if (userType === 'ORGANIZER') {
      return null;
    }

    // Dựa vào prop `applicationStatus` để quyết định
    switch (applicationStatus) {
      // TRẠNG THÁI: CHỜ DUYỆT
      case 'applied':
        return (
          <div className="flex items-center space-x-3">
            <div className="bg-yellow-100 text-yellow-800 font-bold py-2 px-6 rounded-lg cursor-default">
              Chờ duyệt
            </div>
            <button
              onClick={onCancelClick}
              className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-6 rounded-lg shadow-md"
            >
              Hủy
            </button>
          </div>
        );

      // TRẠNG THÁI: ĐÃ ĐƯỢC DUYỆT
      case 'approved':
        return (
          <div className="bg-green-100 text-green-800 font-bold py-2 px-6 rounded-lg cursor-default">
            Đã duyệt
          </div>
        );

      // TRẠNG THÁI: ĐÃ THAM GIA (hoặc vắng mặt, đã hoàn thành)
      case 'attended':
      case 'absent':
        return (
          <div className="bg-gray-200 text-gray-700 font-bold py-2 px-6 rounded-lg cursor-default">
            Đã hoàn thành
          </div>
        );

      // TRẠNG THÁI: BỊ TỪ CHỐI (hoặc đã hủy)
      case 'rejected':
      case 'withdrawn':
        return (
          <div className="bg-red-100 text-red-800 font-bold py-2 px-6 rounded-lg cursor-default">
            Đã từ chối / Hủy
          </div>
        );

      // TRƯỜNG HỢP MẶC ĐỊNH: Chưa đăng ký (status là null hoặc undefined)
      default:
        return (
          <button
            onClick={onRegisterClick}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg shadow-md"
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
          <span className="text-blue-700">{activity.title}</span>
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