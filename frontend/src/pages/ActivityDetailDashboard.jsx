import React from 'react';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import ActivityStats from '../components/activity/ActivityStats';
import ActivityContent from '../components/activity/ActivityContent';
import ActivityDetailDashboardHeader from '../components/activity/ActivityDetailDashboardHeader';
import { useParams, useNavigate } from 'react-router-dom';
import { allActivitiesDetails } from '../mockdata/mockActivities'; 


function ActivityDetailDashboard() {
  const { activityId } = useParams();
  const navigate = useNavigate();
  const selectedActivity = allActivitiesDetails[activityId];
  const handleModifyClick = () => {
    console.log(`Chỉnh sửa hoạt động ID: ${selectedActivity.id}`);
    alert(`Bạn đã sửa thông tin hoạt động "${selectedActivity.title}" (Đây là demo).`);
  };
  const handleDeleteClick = () => {
    console.log(`Xóa hoạt động ID: ${selectedActivity.id}`);
    alert(`Bạn đã xóa hoạt động "${selectedActivity.title}" (Đây là demo).`);
  };

  if (!selectedActivity) {
    return <div>Hoạt động không tồn tại!</div>;
  }

  return (
    <>
        <div className="mb-6">
          <button 
             onClick={() => navigate(-1)}
            className="flex items-center text-gray-700 font-bold font-serif hover:text-blue-600 transition-colors duration-200"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Quay về
          </button>
        </div>
        
        <ActivityDetailDashboardHeader
          activity={selectedActivity}
          onModifyClick={handleModifyClick}
          onDeleteClick={handleDeleteClick}
        />

        <div className="bg-white p-6 mt-6 rounded-x1 shadow-md border border-gray-200">
          <ActivityStats 
            maxDays={selectedActivity.stats.maxDays} 
            approvedDays={selectedActivity.stats.approvedDays} 
            duration={selectedActivity.stats.duration} 
          />
          <hr className="my-4 border-gray-300" />
          <ActivityContent details={selectedActivity.details} />
        </div>
      </>
  );
}

export default ActivityDetailDashboard;