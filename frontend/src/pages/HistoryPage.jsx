// src/pages/HistoryActivitiesPage.jsx

import React from 'react';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import MyActivityListItem from '../components/activity/MyActivityListItem';
import { myActivities } from '../mockdata/mockActivities';
import { useNavigate } from 'react-router-dom';

function HistoryPage() {
  
  const navigate = useNavigate();

  // Lọc ra các hoạt động đã hoàn thành
  const history = myActivities.filter(act => act.status.startsWith('completed'));

  return (
   <>
        <div className="mb-4">
          <button 
            onClick={() => navigate(-1)}
            className="flex items-center text-gray-700 font-bold font-serif hover:text-blue-600 transition-colors duration-200"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Quay về
          </button>
        </div>
        
        <h1 className="text-3xl font-bold font-serif text-center text-gray-800 my-6">
          LỊCH SỬ THAM GIA
        </h1>

        <div className="bg-white p-6 rounded-lg shadow-md">
          {history.length > 0 ? (
            history.map(activity => (
              <MyActivityListItem 
                key={activity.id} 
                activity={activity}
              />
            ))
          ) : (
            <p className="text-center text-gray-500">Lịch sử tham gia của bạn trống.</p>
          )}
        </div>
      </>
  );
}

export default HistoryPage;