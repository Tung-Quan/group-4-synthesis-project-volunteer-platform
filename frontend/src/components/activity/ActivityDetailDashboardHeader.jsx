import React from 'react';

const CloverIcon = () => (
  <span className="text-green-500 text-lg mr-2">🍀</span>
);

function ActivityDetailDashboardHeader({ activity, onModifyClick }) {
let timeFrame = activity.slots?.length > 0
      ? `Từ ${new Date(activity.slots[0].work_date).toLocaleDateString('vi-VN')} đến ${new Date(activity.slots[activity.slots.length - 1].work_date).toLocaleDateString('vi-VN')}`
      : null;

  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
      
      <div className="flex items-center justify-between pb-4 border-b border-gray-200">
        <h1 className="text-xl font-bold">
          <span className="text-blue-700">{activity.title}</span>
        </h1>
        <div className='justify-end space-x-2'>
        <button 
          onClick={onModifyClick}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg shadow-md transition-colors duration-200 whitespace-nowrap"
        >
          Chỉnh sửa
        </button>
        {/*<button 
          onClick={onDeleteClick}
          className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded-lg shadow-md transition-colors duration-200 whitespace-nowrap"
        >
          Xóa
        </button>*/}
        </div>
      </div>

      <div className="flex flex-col space-y-2 pt-4.">
        <div className="flex items-center">
          <CloverIcon />
          <p className="text-gray-700">
            Thời gian: <span className="text-green-600 font-semibold">{timeFrame}</span>
          </p>
        </div>
        
        <div className="flex items-center">
          <CloverIcon />
          <p className="text-gray-700">
            Tại: <span className="text-pink-600 font-semibold">{activity.location}</span>
          </p>
        </div>
      </div>
      
    </div>
  );
}

export default ActivityDetailDashboardHeader;