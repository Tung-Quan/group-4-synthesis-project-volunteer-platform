// src/pages/ParticipatingActivitiesPage.jsx

import React from 'react';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import MyActivityListItem from '../components/activity/MyActivityListItem';
import { myActivities } from '../mockdata/mockActivities';

function ParticipatingPage({ navigateTo, onLogout, isLoggedIn, user }) {
  
  // Lọc ra các hoạt động đang/sắp tham gia
  const participating = myActivities.filter(act => act.status === 'approved' || act.status === 'pending');

  const handleDetailsClick = (activityId) => {
    navigateTo('activity-detail', { id: activityId });
  };
  
  const handleCancelClick = (activityId) => {
    alert(`Bạn có chắc muốn hủy đăng ký hoạt động ${activityId}? (Đây là demo)`);
    // Logic hủy đăng ký sẽ ở đây
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <Header isLoggedIn={isLoggedIn} onLogout={onLogout} user={user} navigateTo={navigateTo} />
      
      <main className="flex-grow max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 w-full">
        <div className="mb-4">
          <button 
            onClick={() => navigateTo('home-logged-in')}
            className="flex items-center text-gray-700 font-bold font-serif hover:text-blue-600 transition-colors duration-200"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Quay về
          </button>
        </div>
        
        <h1 className="text-3xl font-bold font-serif text-center text-gray-800 my-6">
          HOẠT ĐỘNG ĐANG THAM GIA
        </h1>

        <div className="bg-white p-6 rounded-lg shadow-md">
          {participating.length > 0 ? (
            participating.map(activity => (
              <MyActivityListItem 
                key={activity.id} 
                activity={activity}
                onDetailsClick={handleDetailsClick}
                onCancelClick={handleCancelClick}
              />
            ))
          ) : (
            <p className="text-center text-gray-500">Bạn chưa đăng ký tham gia hoạt động nào.</p>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default ParticipatingPage;