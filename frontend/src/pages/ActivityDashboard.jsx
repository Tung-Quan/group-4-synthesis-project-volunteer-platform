import React from 'react';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import ActivityListItem from '../components/activity/ActivityListItem';
import { useNavigate } from 'react-router-dom';
import { managedActivities } from '../mockdata/mockActivities'; // Lấy dữ liệu trực tiếp

function ActivityDashboard() {
  const navigate = useNavigate();

  const handleCreateClick = () => {
    console.log(`Thêm hoạt động mới`);
    // Trong tương lai, đây sẽ là navigate('/organizer/activities/new');
    alert(`Hoạt động được tạo thành công (Đây là demo, chưa hiện thực).`);
  };

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

        <h1 className="text-3xl font-serif font-bold text-center text-gray-800 my-6">
          CÁC HOẠT ĐỘNG ĐANG QUẢN LÝ
        </h1>

        <div className="bg-white p-6 rounded-lg shadow-md">
          {managedActivities.length > 0 ? (
            managedActivities.map(activity => (
              <ActivityListItem 
                key={activity.id} 
                activity={activity}
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
     </>
  );
}

export default ActivityDashboard;