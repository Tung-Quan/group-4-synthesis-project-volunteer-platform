import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import apiClient from "../api/apiClient";
import EventSlot from "../components/activity/EventSlot";

function SeeAppOfEventPage() {
	const { activityId } = useParams();
	const navigate = useNavigate();

	const [error, setError] = useState(null);
	const [activity, setActivity] = useState([]);
	const [isLoading, setIsLoading] = useState(true);

	useEffect(() => {
    const fetchEventToShowSlots = async () => {
      try {
        setIsLoading(true);
        const response = await apiClient.get(`/events/${activityId}`);
        setActivity(response.data);
      } catch (err) {
        if (err.response?.status === 404) {
          setActivity([]);
        } else {
          setError("Không thể tải các ca của hoạt động. Vui lòng thử lại.");
        }
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchEventToShowSlots();
  	},
	[activityId]);

  	if (isLoading) return <div className="text-center p-4">Đang tải...</div>;
	if (error) return <div className="text-center p-4 text-red-500">{error}</div>;

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
          DANH SÁCH CA CỦA HOẠT ĐỘNG: {activity.title}
        </h1>

		{/*an event must have at least 1 slot but this check is for safeguard */}
		<div className="bg-white p-6 rounded-lg shadow-md">
			{slots.length > 0 ? (
			slots.map(slot => <EventSlot key={slot.slot_id} slot={slot}/>)
			) : (
			<p className="text-center text-gray-500">Hoạt động này không có ca nào.</p>
			)}
        </div>
		</>
	);
}

export default SeeAppOfEventPage;