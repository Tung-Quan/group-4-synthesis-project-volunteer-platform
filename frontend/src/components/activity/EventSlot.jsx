import { useParams, useNavigate } from "react-router-dom";

function EventSlot({ slot }) {
	const { activityId } = useParams();
	const navigate = useNavigate();

	const handleViewApplications = () => {
		console.log(`Đang xem hoạt động ID ${activityId}, slot ${slot.slot_id}.`);
		navigate(`/organizer/applications/${activityId}/${slot.slot_id}`);
	}

	return (
		<div className="py-4 border-b border-gray-200 flex items-center justify-between">
		<div>
        <h3 className="text-lg font-semibold text-gray-800 mb-1">Ca ngày: {new Date(slot.work_date).toLocaleDateString('vi-VN', {
                  day: '2-digit', month: '2-digit', year: 'numeric'
                })}</h3>
        <div className="flex space-x-4 text-sm text-gray-600">
          <span>Từ {slot.starts_at} đến {slot.ends_at}</span>
        </div>
      	</div>

		<button onClick={handleViewApplications}
		className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200">
			Xem danh sách
		</button>
		</div>
	);
}

export default EventSlot;