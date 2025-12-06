import React, { useEffect, useState } from 'react';
import ApplicationEventListItem from '../components/application/ApplicationEventListItem';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/apiClient';

//Make it show events and their shifts, then shows the applications when selecting a shift (slot)
//The API call is '/applications/{event_id}/slots/{slot_id}'
//Select in order: Event -> Slot -> Applications
function ApplicationReviewPage() {
    const navigate = useNavigate();

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

  if (isLoading) return <div className="text-center p-4">Đang tải...</div>;
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
          DANH SÁCH HOẠT ĐỘNG NHẬN ĐƠN
        </h1>

        <div className="bg-white p-6 rounded-lg shadow-md">
          {activities.length > 0 ? (
            activities.map(a => (
              <ApplicationEventListItem 
                key={a.id}
                event={a}
              />
            ))
          ) : (
            <p className="text-center text-gray-500">Hiện bạn không có quản lý hoạt động nào.</p>
          )}
        </div>
      </>
  );
}

export default ApplicationReviewPage;