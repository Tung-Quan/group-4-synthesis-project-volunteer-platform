// import React, { useState } from 'react';
// import Header from '../components/common/Header';
// import Footer from '../components/common/Footer';
// import ActivityDetailHeader from '../components/activity/ActivityDetailHeader';
// import ActivityStats from '../components/activity/ActivityStats';
// import ActivityContent from '../components/activity/ActivityContent';
// import ShiftsModal from '../components/activity/ShiftsModal'; // 2. IMPORT MODAL

// import { useParams, useNavigate } from 'react-router-dom';
// import { allActivitiesDetails, myActivities } from '../mockdata/mockActivities';

// function ActivityDetailPage({user}) {
//   const [isModalOpen, setIsModalOpen] = useState(false);
//   const navigate = useNavigate();
//   const { activityId } = useParams(); //Lấy ID từ URL
//   const selectedActivity = allActivitiesDetails[activityId]; 
//   // khi dùng API thật thì gọi API, useEfffect và fetch ở đây

//   const userApplicationStatus = myActivities.find(
//     activity => activity.id === activityId
//   )?.status || null;

//   const handleRegisterClick = () => {
//     setIsModalOpen(true);
//   };

//   const handleRegisterShift = (shiftId) => {
//     console.log(`Đang đăng ký ca ${shiftId} cho hoạt động ${selectedActivity.id}`);
//     alert(`Đăng ký thành công ca ${shiftId} cho hoạt động "${selectedActivity.title}"! (Đây là demo)`);
//     setIsModalOpen(false);
//     // Trong tương lai, đây là nơi bạn sẽ gọi API POST /events/apply với shift_id
//   };

//   const handleCancelClick = () => {
//     alert(`Bạn có chắc muốn hủy đăng ký hoạt động ${selectedActivity.id}? (Đây là demo)`);
//   };

//   if (!selectedActivity) {
//     return (
//       <div className="text-center p-10">
//         <h1 className="text-2xl font-bold">404 - Hoạt động không tồn tại</h1>
//         <button onClick={() => navigate('/')} className="mt-4 text-blue-600 hover:underline">
//           Quay về trang chủ
//         </button>
//       </div>
//     );
//   }

//   return (
//       <>
//         <div className="mb-6">
//           <button 
//              onClick={() => navigate(-1)}
//             className="flex items-center text-gray-700 font-bold font-serif hover:text-blue-600 transition-colors duration-200"
//           >
//             <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
//             Quay về
//           </button>
//         </div>
        
//         <ActivityDetailHeader 
//           activity={selectedActivity}
//           onRegisterClick={handleRegisterClick}
//           userType={user.type}
//           applicationStatus={userApplicationStatus}
//           onCancelClick={handleCancelClick}
//         />

//         <div className="bg-white p-6 mt-6 rounded-x1 shadow-md border border-gray-200">
//           <ActivityStats 
//             maxDays={selectedActivity.stats.maxDays} 
//             approvedDays={selectedActivity.stats.approvedDays} 
//             duration={selectedActivity.stats.duration} 
//           />
//           <hr className="my-4 border-gray-300" />
//           <ActivityContent details={selectedActivity.details} />
//         </div>
        
//         <ShiftsModal
//           isOpen={isModalOpen}
//           onClose={() => setIsModalOpen(false)}
//           shifts={selectedActivity.shifts}
//           onRegisterShift={handleRegisterShift}
//           activityTitle={selectedActivity.title}
//         />
//       </>
//   );
// }

// export default ActivityDetailPage;

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../api/apiClient';
import { useAuth } from '../context/AuthContext';

import ActivityDetailHeader from '../components/activity/ActivityDetailHeader';
import ActivityContent from '../components/activity/ActivityContent';
import ShiftsModal from '../components/activity/ShiftsModal';

function ActivityDetailPage() {
  const { user } = useAuth();
  const { activityId } = useParams();
  const navigate = useNavigate();

  const [activity, setActivity] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // TODO: Cần một API để lấy trạng thái đăng ký của user cho hoạt động này
  const userApplicationStatus = null; // Tạm thời để là null

  useEffect(() => {
    const fetchActivityDetail = async () => {
      if (!activityId) return;
      try {
        setIsLoading(true);
        setError(null);
        const response = await apiClient.get(`/events/${activityId}`);
        setActivity(response.data);
      } catch (err) {
        setError("Không thể tải thông tin hoạt động này.");
        console.error(`Error fetching activity ${activityId}:`, err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchActivityDetail();
  }, [activityId]);

  const handleRegisterShift = async (slotId) => {
    try {
      await apiClient.post('/applications/apply', {
        event_id: activityId,
        slot_id: slotId,
        note: "Applied from web"
      });
      alert(`Đăng ký thành công ca làm việc!`);
      setIsModalOpen(false);
      // Tải lại trang để cập nhật trạng thái
      window.location.reload();
    } catch (err) {
      alert(`Đăng ký thất bại: ${err.response?.data?.detail || 'Có lỗi xảy ra.'}`);
    }
  };

  if (isLoading) return <div className="text-center p-4">Đang tải chi tiết hoạt động...</div>;
  if (error) return <div className="text-center p-4 text-red-500">{error}</div>;
  if (!activity) return <div className="text-center p-4">Không tìm thấy hoạt động.</div>;

  const headerProps = {
    id: activity.id,
    title: activity.title,
    time: activity.slots?.length > 0
      ? `Từ ${new Date(activity.slots[0].work_date).toLocaleDateString('vi-VN')} đến ${new Date(activity.slots[activity.slots.length - 1].work_date).toLocaleDateString('vi-VN')}`
      : null,
    locationDetail: activity.location,
  };

  const shiftsForModal = (activity.slots || []).map(slot => ({
    id: slot.slot_id,
    time: `${slot.starts_at.substring(0, 5)} - ${slot.ends_at.substring(0, 5)} ngày ${new Date(slot.work_date).toLocaleDateString('vi-VN')}`,
    location: activity.location,
    capacity: slot.capacity,
    // TODO: API cần trả về số lượng đã đăng ký cho từng slot
    registered: slot.approved_count || 0, // Giả sử API trả về `approved_count`
  }));

  return (
    <>
      <div className="mb-6">
        <button onClick={() => navigate(-1)} className="flex items-center text-gray-700 font-bold font-serif hover:text-blue-600 transition-colors duration-200">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
          Quay về
        </button>
      </div>

      <ActivityDetailHeader
        activity={headerProps}
        onRegisterClick={() => setIsModalOpen(true)}
        userType={user?.type}
        applicationStatus={userApplicationStatus}
        onCancelClick={() => alert("Chức năng hủy đang được phát triển")}
      />

      <div className="bg-white p-6 mt-6 rounded-xl shadow-md border border-gray-200">
        <ActivityContent
          description={activity.description}
          location={activity.location}
        />
      </div>

      <ShiftsModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        shifts={shiftsForModal}
        onRegisterShift={handleRegisterShift}
        activityTitle={activity.title}
      />
    </>
  );
}

export default ActivityDetailPage;