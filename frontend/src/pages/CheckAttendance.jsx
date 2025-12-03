import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import apiClient from "../api/apiClient";
import AttendVolunteer from "../components/attendance/AttendVolunteer";

function CheckAttendance() {
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

        const validApps = appRes.data.filter(s => s.status === "approved");
        setApplications(validApps);
        
		setActivity(eventRes.data);
		setSlot(slotRes.data);
      } catch (err) {
        if (err.response?.status === 404) {
          setApplications([]);
		  setActivity([]);
		  setSlot([]);
        } else {
          setError("Không thể tải các hồ sơ được gửi về. Vui lòng thử lại.");
        }
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchApplicationInSlot();
  	}, [activityId, slotId]);

  	if (isLoading) return <div className="text-center p-4">Đang tải các hồ sơ...</div>;
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
          ĐIỂM DANH HOẠT ĐỘNG {activity.title}
        </h1>
		    <h2 className="text-2xl font-serif font-bold text-center text-gray-700 my-4">
          CA NGÀY {new Date(slot.work_date).toLocaleDateString('vi-VN', {
                  day: '2-digit', month: '2-digit', year: 'numeric'
                })} TỪ {slot.starts_at?.substring(0, 5)} ĐẾN {slot.ends_at?.substring(0, 5)}
        </h2>

		<div className="bg-white p-6 rounded-lg shadow-md">
		{/*
			react.js freaks out when trying to preprocess earlier
			also still gives no data when empty response
		*/}
			{applications.filter(a => (a.status === "approved")).length > 0 ? (
				applications.filter(a => (a.status === "approved")).map(a => <AttendVolunteer key={a.student_no} volunteer={a}/>)
			) : (
			<p className="text-center text-gray-500">Danh sách điểm danh trống.</p>
			)}
        </div>
		</>
	);
}

export default CheckAttendance;