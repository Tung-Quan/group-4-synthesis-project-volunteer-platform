import React from "react";

function RecentUpdate(activities)
{
	//Placeholder statuses, will change to match backend implementation later in development
	const statusToText = (s) => {
		switch (s) {
			case "InfoUpdated":
				return "đã được cập nhật";

			case "NoRegister":
				return "hết hạn đăng ký";

			default:
				break;
		}
	};

	return (
		<div className="bg-gray-800 p-5 rounded-lg shadow-xl">
		<h2 className="text-blue-600 font-semibold text-l mb-2">Cập nhật gần đây</h2>
		<div className="space-y-3 max-h-64 pr-2"> 
		<ul>
			{activities.map((activity) => (
			<li key={activity.id}>
				Hoạt động {activity.title} {statusToText(activity.status)}.
			</li>
			))}
		</ul>
		</div>
		</div>
	);
}

export default RecentUpdate;