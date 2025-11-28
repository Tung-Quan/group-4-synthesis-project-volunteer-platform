// import React from 'react';
// import { useNavigate } from 'react-router-dom';

// // Component nhỏ để hiển thị trạng thái
// const StatusBadge = ({ status }) => {
//   const statusStyles = {
//     approved: 'bg-green-100 text-green-800',
//     pending: 'bg-yellow-100 text-yellow-800',
//     rejected: 'bg-red-100 text-red-800',
//     'completed-attended': 'bg-blue-100 text-blue-800',
//     'completed-absent': 'bg-gray-200 text-gray-800',
//   };
//   const statusTexts = {
//     approved: 'Đã duyệt',
//     pending: 'Chờ duyệt',
//     rejected: 'Bị từ chối',
//     'completed-attended': 'Đã tham gia',
//     'completed-absent': 'Vắng',
//   };
//   return (
//     <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusStyles[status] || 'bg-gray-100'}`}>
//       {statusTexts[status] || 'Không xác định'}
//     </span>
//   );
// };

// function MyActivityListItem({ activity, onCancelClick }) {
//   const isUpcoming = activity.status === 'approved' || activity.status === 'pending';
//   const isHistory = activity.status.startsWith('completed');

//   const canCancel = activity.status === 'pending';
//   const navigate = useNavigate();

//   const handleDetailsClick = () => {
//     navigate(`/activities/${activity.id}`);
//   };

//   return (
//     <div className="py-4 border-b border-gray-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
//       {/* Phần thông tin */}
//       <div className="flex-grow">
//         <h3 className="text-lg font-semibold text-gray-800 mb-1">{activity.title}</h3>
//         <div className="flex flex-col sm:flex-row sm:space-x-4 text-sm text-gray-500">
//           <span>Thời gian: {activity.date}</span>
//           <span>Tại: {activity.location}</span>
//           {/* {isHistory && activity.recordedDays !== undefined && (
//             <span className="font-semibold text-green-600">CTXH được ghi nhận: {activity.recordedDays} ngày</span>
//           )} */}
//         </div>
//       </div>

//       {/* Phần trạng thái và nút bấm */}
//       <div className="flex items-center space-x-3 flex-shrink-0">
//         <div className="flex flex-col items-end"> 
//           <StatusBadge status={activity.status} />
//           {isHistory && activity.recordedDays !== undefined && (
//             <span className="text-xs font-semibold text-green-600 mt-1">
//               CTXH: {activity.recordedDays} ngày
//             </span>
//           )}
//         </div>
//         {isUpcoming && (
//           <>
//             <button 
//               onClick={handleDetailsClick}
//               className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
//             >
//               Chi tiết
//             </button>
//             <button
//               onClick={() => canCancel && onCancelClick(activity.id)} 
//               // Thay đổi class và thêm thuộc tính 'disabled'
//               className={`font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200
//                 ${canCancel 
//                   ? 'bg-red-500 hover:bg-red-600 text-white' 
//                   : 'bg-gray-300 text-gray-500 cursor-not-allowed'
//                 }
//               `}
//               disabled={!canCancel} // Vô hiệu hóa nút nếu không thể hủy
//             >
//               Hủy
//             </button>
//           </>
//         )}
//         {isHistory && (
//            <button 
//             onClick={handleDetailsClick}
//             className="bg-gray-500 hover:bg-gray-600 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
//           >
//             Xem lại
//           </button>
//         )}
//       </div>
//     </div>
//   );
// }

// export default MyActivityListItem;


// import React from 'react';
// import { useNavigate } from 'react-router-dom';

// // Component StatusBadge không thay đổi, nó vẫn hoạt động tốt
// const StatusBadge = ({ status }) => {
//   const statusStyles = {
//     approved: 'bg-green-100 text-green-800',
//     applied: 'bg-yellow-100 text-yellow-800', // Thêm 'applied' từ API
//     attended: 'bg-blue-100 text-blue-800', // Thêm 'attended' từ API
//     absent: 'bg-gray-200 text-gray-800', // Thêm 'absent' từ API
//     rejected: 'bg-red-100 text-red-800',
//     withdrawn: 'bg-orange-100 text-orange-800', // Thêm 'withdrawn' từ API
//   };
//   const statusTexts = {
//     approved: 'Đã duyệt',
//     applied: 'Chờ duyệt',
//     attended: 'Đã tham gia',
//     absent: 'Vắng',
//     rejected: 'Bị từ chối',
//     withdrawn: 'Đã rút đơn',
//   };
//   return (
//     <span className={`px-2 py-1 text-xs font-semibold rounded-full w-fit ${statusStyles[status] || 'bg-gray-100'}`}>
//       {statusTexts[status] || status || 'Không xác định'}
//     </span>
//   );
// };


// function MyActivityListItem({ application, onCancelClick }) {
//   const navigate = useNavigate();

//   const isUpcoming = application.status === 'approved' || application.status === 'applied';
//   const isHistory = application.status === 'attended' || application.status === 'absent';
//   const canCancel = application.status === 'applied';

//   const handleDetailsClick = () => {
//     if (application.event_id) {
//       navigate(`/activities/${application.event_id}`);
//     } else {
//       alert("Không thể xem chi tiết lúc này.");
//     }
//   };

//   return (
//     <div className="py-4 border-b border-gray-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
//       {/* Phần thông tin */}
//       <div className="flex-grow">
//         <h3 className="text-lg font-semibold text-gray-800 mb-1">{application.event_name}</h3>
//         <div className="flex flex-col sm:flex-row sm:space-x-4 text-sm text-gray-500">
//           <span>Ngày: {new Date(application.work_date).toLocaleDateString('vi-VN')}</span>
//           <span>Thời gian: {application.starts_at.substring(0, 5)} - {application.ends_at.substring(0, 5)}</span>
//           <span>Tại: {application.location}</span>
//         </div>
//       </div>

//       <div className="flex items-center space-x-3 flex-shrink-0">
//         <div className="flex flex-col items-end">
//           <StatusBadge status={application.status} />
//         </div>

//         {isUpcoming && (
//           <>
//             <button
//               onClick={handleDetailsClick}
//               className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
//             >
//               Chi tiết
//             </button>
//             <button
//               onClick={() => canCancel && onCancelClick(application)}
//               className={`font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200
//                 ${canCancel
//                   ? 'bg-red-500 hover:bg-red-600 text-white'
//                   : 'bg-gray-300 text-gray-500 cursor-not-allowed'
//                 }
//               `}
//               disabled={!canCancel}
//             >
//               Hủy
//             </button>
//           </>
//         )}

//         {isHistory && (
//           <button
//             onClick={handleDetailsClick}
//             className="bg-gray-500 hover:bg-gray-600 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200"
//           >
//             Xem lại
//           </button>
//         )}
//       </div>
//     </div>
//   );
// }

// export default MyActivityListItem;



import React from 'react';
import { useNavigate } from 'react-router-dom';

const StatusBadge = ({ status }) => {
  const statusStyles = {
    approved: 'bg-green-100 text-green-800',
    applied: 'bg-yellow-100 text-yellow-800', 
    rejected: 'bg-red-100 text-red-800',
    withdrawn: 'bg-gray-200 text-gray-700', // Trạng thái mới: đã rút đơn
    attended: 'bg-blue-100 text-blue-800',  // Trạng thái mới: đã tham gia
    absent: 'bg-purple-100 text-purple-800', // Trạng thái mới: vắng mặt
  };
  const statusTexts = {
    approved: 'Đã duyệt',
    applied: 'Chờ duyệt',
    rejected: 'Bị từ chối',
    withdrawn: 'Đã hủy',
    attended: 'Đã tham gia',
    absent: 'Vắng mặt',
  };
  return (
    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusStyles[status] || 'bg-gray-100'}`}>
      {statusTexts[status] || status}
    </span>
  );
};

function MyActivityListItem({ application, onCancelClick }) {
  const navigate = useNavigate();

  const isHistory = ['attended', 'absent', 'rejected', 'withdrawn'].includes(application.status);
  const isUpcoming = ['applied', 'approved'].includes(application.status);
  const canCancel = application.status === 'applied';

  const handleDetailsClick = () => {
    if (application.event_id) {
      navigate(`/activities/${application.event_id}`);
    } else {
      alert("Lỗi: Không tìm thấy ID của hoạt động.");
    }
  };

  return (
    <div className="py-4 border-b border-gray-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div className="flex-grow">
        <h3 className="text-lg font-semibold text-gray-800 mb-1">{application.event_name}</h3>
        <div className="flex flex-col sm:flex-row sm:space-x-4 text-sm text-gray-500">
          <span>Ngày: {new Date(application.work_date).toLocaleDateString('vi-VN')}</span>
          <span>Thời gian: {application.starts_at.substring(0, 5)} - {application.ends_at.substring(0, 5)}</span>
          <span>Tại: {application.location}</span>
        </div>
      </div>

      <div className="flex items-center space-x-3 flex-shrink-0">
        <StatusBadge status={application.status} />

        {isUpcoming && (
          <>
            <button
              onClick={handleDetailsClick}
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md"
            >
              Chi tiết
            </button>
            <button
              onClick={() => onCancelClick(application)}
              className={`font-bold text-sm py-1.5 px-4 rounded-full shadow-md transition-colors duration-200
                ${canCancel
                  ? 'bg-red-500 hover:bg-red-600 text-white'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }
              `}
              disabled={!canCancel}
            >
              Hủy
            </button>
          </>
        )}
        {isHistory && (
          <button
            onClick={handleDetailsClick}
            className="bg-gray-500 hover:bg-gray-600 text-white font-bold text-sm py-1.5 px-4 rounded-full shadow-md"
          >
            Xem lại
          </button>
        )}
      </div>
    </div>
  );
}

export default MyActivityListItem;