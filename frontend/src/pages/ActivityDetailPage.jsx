import React, { useState } from 'react';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import ActivityDetailHeader from '../components/activity/ActivityDetailHeader';
import ActivityStats from '../components/activity/ActivityStats';
import ActivityContent from '../components/activity/ActivityContent';
import ShiftsModal from '../components/activity/ShiftsModal'; // 2. IMPORT MODAL

import { useParams, useNavigate } from 'react-router-dom';
import { allActivitiesDetails, myActivities } from '../mockdata/mockActivities';

function ActivityDetailPage({user}) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();
  const { activityId } = useParams(); //Lấy ID từ URL
  const selectedActivity = allActivitiesDetails[activityId]; 
  // khi dùng API thật thì gọi API, useEfffect và fetch ở đây

  const userApplicationStatus = myActivities.find(
    activity => activity.id === activityId
  )?.status || null;

  const handleRegisterClick = () => {
    setIsModalOpen(true);
  };

  const handleRegisterShift = (shiftId) => {
    console.log(`Đang đăng ký ca ${shiftId} cho hoạt động ${selectedActivity.id}`);
    alert(`Đăng ký thành công ca ${shiftId} cho hoạt động "${selectedActivity.title}"! (Đây là demo)`);
    setIsModalOpen(false);
    // Trong tương lai, đây là nơi bạn sẽ gọi API POST /events/apply với shift_id
  };

  const handleCancelClick = () => {
    alert(`Bạn có chắc muốn hủy đăng ký hoạt động ${selectedActivity.id}? (Đây là demo)`);
  };

  if (!selectedActivity) {
    return (
      <div className="text-center p-10">
        <h1 className="text-2xl font-bold">404 - Hoạt động không tồn tại</h1>
        <button onClick={() => navigate('/')} className="mt-4 text-blue-600 hover:underline">
          Quay về trang chủ
        </button>
      </div>
    );
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
        
        <ActivityDetailHeader 
          activity={selectedActivity}
          onRegisterClick={handleRegisterClick}
          userType={user.type}
          applicationStatus={userApplicationStatus}
          onCancelClick={handleCancelClick}
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
        
        <ShiftsModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          shifts={selectedActivity.shifts}
          onRegisterShift={handleRegisterShift}
          activityTitle={selectedActivity.title}
        />
      </>
  );
}

export default ActivityDetailPage;