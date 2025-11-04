import React from 'react';
import { getUserDisplayName } from '../../mockdata/mockUser';
import { getTitle } from '../../mockdata/mockActivities';

function ApplicationListItem({ application, onDetailsClick }) {

  return (
    <div className="py-4 border-b border-gray-200 flex items-center justify-between">
      <div>
        <h3 className="text-base font-semibold text-gray-800 mb-1">{getTitle(application.activityId)}</h3>
        <div className="flex space-x-4 text-sm text-gray-500">
          <span>Thời gian gửi: {application.timeSent}</span>
          <span>Tên ứng viên: {getUserDisplayName(application.volunteerId)}</span>
        </div>
      </div>

      <button 
        onClick={() => onDetailsClick(application.id)}
        className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
      >
        Chi tiết
      </button>
      
    </div>
  );
}

export default ApplicationListItem;