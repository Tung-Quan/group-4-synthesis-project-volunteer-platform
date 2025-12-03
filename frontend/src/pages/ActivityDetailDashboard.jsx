import React, { useState, useEffect } from 'react';
import ActivityDetailDashboardHeader from '../components/activity/ActivityDetailDashboardHeader';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../api/apiClient';
import AttendancePerSlotItem from '../components/attendance/AttendancePerSlotItem';

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

  function compareTime(slot1, slot2) {
		//we abusing strings with this one
		let date1 = new Date(slot1.work_date + 'T' + slot1.starts_at);
		let date2 = new Date(slot2.work_date + 'T' + slot2.starts_at);

		if (date1 < date2) {
			return -1;
		}
		else if (date2 > date1) {
			return 1;
		}
		else {
			return 0;
		}
	}
	const slots = activity.slots.sort(compareTime);

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
          <div className="space-y-1 text-base">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Nội dung hoạt động</h2>
            <div className="flex flex-col sm:flex-row py-2 border-b border-gray-200 last:border-b-0">
              <span className="text-gray-700 break-words">{activity.description}</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 mt-6 rounded-x1 shadow-md border border-gray-200">
          <div className="space-y-1 text-base">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Các ca hoạt động</h2>
          </div>
          <hr></hr>
          {
            slots.map((slot, index) => {
              return <AttendancePerSlotItem key={slot.slot_id} slot={slot} index={index + 1}/>
            })
          }
        </div>
      </>
  );
}

export default ActivityDetailDashboard;