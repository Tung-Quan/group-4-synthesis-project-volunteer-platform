import React, { useState, useEffect } from 'react';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';

import { useNavigate } from 'react-router-dom';

function CreateNewActivityPage() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const selectedActivity = 1;

  /*const userApplicationStatus = myActivities.find(
    activity => activity.id === activityId
  )?.status || null;

  /*const handleCreateClick = () => {
    console.log(`Đã tạo hoạt động mới.`);
    alert(`Tạo hoạt động mới thành công.`);
  }*/
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

export default CreateNewActivityPage;