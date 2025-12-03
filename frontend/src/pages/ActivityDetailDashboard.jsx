import React, { useState, useEffect } from 'react';
import ActivityContent from '../components/activity/ActivityContent';
import ActivityDetailDashboardHeader from '../components/activity/ActivityDetailDashboardHeader';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../api/apiClient';

function ActivityDetailDashboard() {
  const { activityId } = useParams();
  const navigate = useNavigate();

  const [activity, setActivity] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

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

  if (isLoading) return <div className="text-center p-4">Đang tải chi tiết hoạt động...</div>;
  if (error) return <div className="text-center p-4 text-red-500">{error}</div>;
  if (!activity) return <div className="text-center p-4">Không tìm thấy hoạt động.</div>;

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
          activity={activity}
          onModifyClick={/*() => setIsEditModalOpen(true)*/ () => navigate(`/organizer/dashboard/${activityId}/edit`)}
        />

        <div className="bg-white p-6 mt-6 rounded-x1 shadow-md border border-gray-200">
          {/*<ActivityStats 
            maxDays={selectedActivity.stats.maxDays} 
            approvedDays={selectedActivity.stats.approvedDays} 
            duration={selectedActivity.stats.duration} 
          />
          <hr className="my-4 border-gray-300" />*/}
          <ActivityContent description={activity.description} location={activity.location}/>
        </div>
      </>
  );
}

export default ActivityDetailDashboard;