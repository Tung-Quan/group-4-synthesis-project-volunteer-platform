import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import apiClient from "../../api/apiClient";

function EventSlot( { slot } ) {
	const { activityId } = useParams();
	const navigate = useNavigate();
	const [open, setOpen] = useState(false);

	const [applications, setApplications] = useState([]);
	const [error, setError] = useState(null);
	const [isLoading, setIsLoading] = useState(true);

	useEffect(() => {
    const fetchApplicationInSlot = async () => {
      try {
        setIsLoading(true);
        const response = await apiClient.get(`/applications/${activityId}/${slot.slot_id}`);
        setApplications(response.data);
		console.log(response.data);
      } catch (err) {
        if (err.response?.status === 404) {
          setApplications([]);
        } else {
          setError("Không thể tải các hồ sơ được gửi về. Vui lòng thử lại.");
        }
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchApplicationInSlot();
  }, [activityId, slot.slot_id]);

	const toggleListDropdown = () => {
		setOpen(!open);
	};

	if (isLoading) return <div className="text-center p-4">Đang tải...</div>;
	if (error) return <div className="text-center p-4 text-red-500">{error}</div>;

	return (
		<div className="py-4 border-b border-gray-200 flex items-center justify-between">
		<button onClick={toggleListDropdown}
		className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200">
			{open ? "Đóng" : "Xem danh sách"}
		</button>
		{open && (
			<div>
				<h4>{slot.work_date}</h4>
			</div>
		)}
		</div>
	);
}

export default EventSlot;