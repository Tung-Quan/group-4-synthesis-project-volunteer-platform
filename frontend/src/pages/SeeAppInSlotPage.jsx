import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import apiClient from "../api/apiClient";
import ApplicationListItem from "../components/application/ApplicationListItem";

function SeeAppInSlotPage() {
	const { activityId, slotId } = useParams();
	const navigate = useNavigate();

	const [error, setError] = useState(null);
	const [applications, setApplications] = useState([]);
	const [isLoading, setIsLoading] = useState(true);

	//auxillary
	const [activity, setActivity] = useState(null);
	const [slot, setSlot] = useState(null);
	
	useEffect(() => {
    const fetchApplicationInSlot = async () => {
      try {
        setIsLoading(true);
        
        // Dùng Promise.all để gọi song song 
        const [appRes, eventRes, slotRes] = await Promise.all([
            apiClient.get(`/applications/${activityId}/slots/${slotId}`), 
            apiClient.get(`/events/${activityId}`),
            apiClient.get(`/events/slots/${slotId}`)
        ]);

        // ọc dữ liệu NGAY LÚC LẤY VỀ 
        const validApps = appRes.data.filter(s => s.status === "applied");
        setApplications(validApps);
        
		setActivity(eventRes.data);
		setSlot(slotRes.data);

      } catch (err) {
        // thông báo nếu có lỗi 404 xảy ra (không có event/slot này) 
        console.error(err);
        setError("Có lỗi xảy ra hoặc không tìm thấy dữ liệu.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchApplicationInSlot();
  	}, [activityId, slotId]);

  	if (isLoading) return <div className="text-center p-4">Đang tải các hồ sơ...</div>;
	  if (error) return <div className="text-center p-4 text-red-500">{error}</div>;
    
    console.log(slot);

    // kiểm tra dữ liệu null trước khi render để tránh crash "Cannot read properties of null"
    if (!activity || !slot) {
        return <div className="text-center p-4 text-gray-500">Không tìm thấy thông tin hoạt động hoặc ca này.</div>;
    }

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
          DANH SÁCH ĐĂNG KÝ: {activity.title}
        </h1>
		<h2 className="text-2xl font-serif font-bold text-center text-gray-700 my-4">
          CA NGÀY {slot.work_date} TỪ {slot.starts_at?.substring(0, 5)} ĐẾN {slot.ends_at?.substring(0, 5)}
        </h2>

		<div className="bg-white p-6 rounded-lg shadow-md">
      {/*
        react.js freaks out when trying to preprocess earlier
        also still gives no data when empty response
      */}
			{applications.filter(s => (s.status === "applied")).length > 0 ? (
				applications.filter(s => (s.status === "applied")).map(a => <ApplicationListItem key={a.student_no} application={a}/>)
			) : (
			<p className="text-center text-gray-500">Hiện ca này không có đơn nào chờ duyệt.</p>
			)}
        </div>
		</>
	);
}

export default SeeAppInSlotPage;