import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ActivityListItem from '../components/activity/ActivityListItem';
import apiClient from '../api/apiClient';

function NewActivitiesPage() {
  const navigate = useNavigate();
  const [activities, setActivities] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUpcomingEvents = async () => {
      try {
        setIsLoading(true);
        const response = await apiClient.get('/events/upcoming');
        setActivities(response.data);
      } catch (err) {
        if (err.response?.status === 404) {
          setActivities([]); 
          setError("Không thể tải danh sách hoạt động. Vui lòng thử lại.");
        }
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUpcomingEvents();
  }, []);

  if (isLoading) return <div>Đang tải các hoạt động mới...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

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
        HOẠT ĐỘNG MỚI
      </h1>

      <div className="bg-white p-6 rounded-lg shadow-md">
        {activities.length > 0 ? (
          activities.map(activityFromApi => {
            let formattedDate = 'Chưa có thông tin';
            if (activityFromApi.event_start_time) {
              try {
                formattedDate = new Date(activityFromApi.event_start_time).toLocaleDateString('vi-VN', {
                  day: '2-digit',
                  month: '2-digit',
                  year: 'numeric',
                });
              } catch (e) {
                console.error("Invalid date format from API:", activityFromApi.event_start_time);
              }
            }

            const activityProps = {
              id: activityFromApi.id,
              title: activityFromApi.title || 'Hoạt động không có tiêu đề',
              date: formattedDate,
              location: activityFromApi.location || 'Chưa có địa điểm',
            };

            return (
              <ActivityListItem
                key={activityFromApi.id}
                activity={activityProps}
              />
            );
          })
        ) : (
          <p className="text-center text-gray-500">Không có hoạt động mới nào sắp diễn ra.</p>
        )}
      </div>
    </>
  );
}

export default NewActivitiesPage;