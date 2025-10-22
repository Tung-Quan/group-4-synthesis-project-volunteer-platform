import React from 'react';
import { getUserDisplayName } from '../../mockdata/mockUser';
import { getTitle } from '../../mockdata/mockActivities';

function ApplicationDetailHeader({ application, onAcceptClick, onRejectClick }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
      
      <div className="flex items-center justify-between pb-4 border-b border-gray-200">
        <h1 className="text-xl font-bold">
          <span className="text-blue-700">{getTitle(application.activityId)}</span>
        </h1>
        <div className='justify-end space-x-2'>
        <button 
          onClick={onAcceptClick}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg shadow-md transition-colors duration-200 whitespace-nowrap"
        >
          Đồng ý
        </button>
        <button 
          onClick={onRejectClick}
          className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded-lg shadow-md transition-colors duration-200 whitespace-nowrap"
        >
          Từ chối
        </button>
        </div>
      </div>

      <div className="flex flex-col space-y-2 pt-4.">
        <div className="flex items-center">
          <p className="text-gray-700">
            Thời gian gửi: <span className="text-green-600 font-semibold">{application.timeSent}</span>
          </p>
        </div>
        
        <div className="flex items-center">
          <p className="text-gray-700">
            Tên ứng viên: <span className="text-cyan-500 font-semibold">{getUserDisplayName(application.volunteerId)}</span>
          </p>
        </div>
      </div>
      
    </div>
  );
}

export default ApplicationDetailHeader;