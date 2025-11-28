import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/apiClient';
import MyActivityListItem from '../components/activity/MyActivityListItem';

function HistoryPage() {
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setIsLoading(true);
        const response = await apiClient.get('/applications/history');
        setHistory(response.data);
      } catch (err) {
        if (err.response?.status === 404) {
          setHistory([]);
        } else {
          setError("Không thể tải lịch sử tham gia.");
        }
        console.error("Error fetching history:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistory();
  }, []);

  if (isLoading) return <div className="text-center p-4">Đang tải lịch sử...</div>;
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
        LỊCH SỬ THAM GIA
      </h1>

      <div className="bg-white p-6 rounded-lg shadow-md">
        {history.length > 0 ? (
          history.map(item => (
            <MyActivityListItem
              key={`${item.event_id}-${item.slot_id}`}
              application={item}
              onCancelClick={() => { }}
            />
          ))
        ) : (
          <p className="text-center text-gray-500">Lịch sử tham gia của bạn trống.</p>
        )}
      </div>
    </>
  );
}

export default HistoryPage;