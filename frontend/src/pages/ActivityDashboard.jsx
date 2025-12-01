import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/apiClient';
import DashboardActivityListItem from '../components/activity/DashboardActivityListItem';

function ActivityDashboard() {
  const navigate = useNavigate();

  const handleCreateClick = () => {
    console.log(`Thêm hoạt động mới`);
    navigate('/organizer/activities/new');
  };

  const [error, setError] = useState(null);
  const [activities, setActivities] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchOwnEvents = async () => {
      try {
        setIsLoading(true);
        const response = await apiClient.get('/events/get-own-event');
        setActivities(response.data);
      } catch (err) {
        if (err.response?.status === 404) {
          setActivities([]);
        } else {
          setError("Không thể tải danh sách hoạt động. Vui lòng thử lại.");
        }
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchOwnEvents();
  }, []);

  if (isLoading) return <div className="text-center p-4">Đang tải các hoạt động...</div>;
  if (error) return <div className="text-center p-4 text-red-500">{error}</div>;

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

      <div className="flex justify-center my-6">
        <button 
        onClick={handleCreateClick}
        className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
        >
          Tạo hoạt động mới
        </button>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        {activities.length > 0 ? (
          activities.map(activityFromApi => {
            const activityProps = {
              id: activityFromApi.id,
              title: activityFromApi.title || 'Hoạt động không có tiêu đề',
              location: activityFromApi.location || 'Chưa có địa điểm',
            };

            return <DashboardActivityListItem key={activityFromApi.id} activity={activityProps} />;
          })
        ) : (
          <p className="text-center text-gray-500">Hiện bạn không quản lý hoạt động nào.</p>
        )}
      </div>
    </>
  );
}

export default ActivityDashboard;