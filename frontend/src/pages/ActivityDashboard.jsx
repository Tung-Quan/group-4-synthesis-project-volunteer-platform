import React from 'react';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import ActivityListItem from '../components/activity/ActivityListItem';

function ActivityDashboard({ navigateTo, onLogout, isLoggedIn, user, activities }) {
  const handleDetailsClick = (activityId) => {
    navigateTo('activity-detail-dashboard', { id: activityId });
  };
  const handleCreateClick = () => {
    console.log(`Thêm hoạt động mới`);
    alert(`Hoạt động được tạo thành công (Đây là demo, chưa hiện thực).`);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <Header
        isLoggedIn={isLoggedIn}
        onLogout={onLogout}
        user={user}
        navigateTo={navigateTo}
      />
      
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

        <h1 className="text-3xl font-serif font-bold text-center text-gray-800 my-6">
          CÁC HOẠT ĐỘNG ĐANG QUẢN LÝ
        </h1>

        <div className="bg-white p-6 rounded-lg shadow-md">
          {activities.length > 0 ? (
            activities.map(activity => (
              <ActivityListItem 
                key={activity.id} 
                activity={activity}
                onDetailsClick={handleDetailsClick}
              />
            ))
          ) : (
			<>
			  <p className="text-center text-gray-500">Không có hoạt động nào.</p>
			  {/* what tag to center? */}
			  <button 
				onClick={handleCreateClick}
				className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
			  >
				Tạo hoạt động mới
			  </button>
			</>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default ActivityDashboard;