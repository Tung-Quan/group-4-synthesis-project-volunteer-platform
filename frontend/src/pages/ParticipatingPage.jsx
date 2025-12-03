import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/apiClient';
import MyActivityListItem from '../components/activity/MyActivityListItem';

function ParticipatingPage() {
  const navigate = useNavigate();
  const [applications, setApplications] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchParticipating = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await apiClient.get('/applications/participating');
      setApplications(response.data);
    } catch (err) {
      if (err.response?.status === 404) {
        setApplications([]);
      } else {
        setError("Không thể tải danh sách hoạt động.");
      }
      console.error("Error fetching participating apps:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchParticipating();
  }, [fetchParticipating]);

  const handleCancelClick = async (applicationToCancel) => {
    const { event_id, slot_id, event_name } = applicationToCancel;

    if (!event_id || !slot_id) {
      alert("Lỗi: Không đủ thông tin để hủy đăng ký. Vui lòng thử lại.");
      return;
    }

    if (window.confirm(`Bạn có chắc muốn hủy đăng ký hoạt động "${event_name}" không?`)) {
      try {
        await apiClient.patch(`/applications/${event_id}/cancel`, { slot_id });
        alert("Hủy đăng ký thành công!");
        fetchParticipating();
      } catch (err) {
        alert(`Hủy thất bại: ${err.response?.data?.detail || 'Có lỗi xảy ra'}`);
      }
    }
  };

  if (isLoading) return <div className="text-center p-4">Đang tải...</div>;
  if (error) return <div className="text-center p-4 text-red-500">{error}</div>;

  return (
    <>
      <div className="mb-4">
        <button onClick={() => navigate(-1)} className="flex items-center text-gray-700 font-bold font-serif hover:text-blue-600 transition-colors duration-200">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
          Quay về
        </button>
      </div>

      <h1 className="text-3xl font-bold font-serif text-center text-gray-800 my-6">
        HOẠT ĐỘNG ĐANG THAM GIA
      </h1>

      <div className="bg-white p-6 rounded-lg shadow-md">
        {applications.length > 0 ? (
          applications.map(app => (
            <MyActivityListItem
              key={`${app.event_id}-${app.slot_id}`} 
              application={app}
              onCancelClick={handleCancelClick}
            />
          ))
        ) : (
          <p className="text-center text-gray-500">Bạn chưa đăng ký tham gia hoạt động nào.</p>
        )}
      </div>
    </>
  );
}

export default ParticipatingPage;