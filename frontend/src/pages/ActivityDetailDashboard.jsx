import React from 'react';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import ActivityStats from '../components/activity/ActivityStats';
import ActivityContent from '../components/activity/ActivityContent';
import ActivityDetailDashboardHeader from '../components/activity/ActivityDetailDashboardHeader';

function ActivityDetailDashboard({ navigateTo, onLogout, isLoggedIn, user, activity, previousPage }) {
  
  const handleModifyClick = () => {
    console.log(`Chỉnh sửa hoạt động ID: ${activity.id}`);
    alert(`Bạn đã sửa thông tin hoạt động "${activity.title}" (Đây là demo).`);
  };
  const handleDeleteClick = () => {
    console.log(`Xóa hoạt động ID: ${activity.id}`);
    alert(`Bạn đã xóa hoạt động "${activity.title}" (Đây là demo).`);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <Header
        isLoggedIn={isLoggedIn}
        onLogout={onLogout}
        user={user}
        navigateTo={navigateTo}
      />
      
      <main className="flex-grow max-w-5xl mx-auto p-4 sm:p-6 lg:p-8 w-full">
        <div className="mb-6">
          <button 
             onClick={() => navigateTo(previousPage || 'home-logged-in')}
            className="flex items-center text-gray-700 font-bold font-serif hover:text-blue-600 transition-colors duration-200"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Quay về
          </button>
        </div>
        
        <ActivityDetailDashboardHeader
          activity={activity}
          onModifyClick={handleModifyClick}
          onDeleteClick={handleDeleteClick}
        />

        <div className="bg-white p-6 mt-6 rounded-x1 shadow-md border border-gray-200">
          <ActivityStats 
            maxDays={activity.stats.maxDays} 
            approvedDays={activity.stats.approvedDays} 
            duration={activity.stats.duration} 
          />
          <hr className="my-4 border-gray-300" />
          <ActivityContent details={activity.details} />
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default ActivityDetailDashboard;