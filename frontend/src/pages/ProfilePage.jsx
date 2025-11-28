// import React, {useMemo, useState} from "react";
// import { useNavigate } from 'react-router-dom';
// import { myActivities } from '../mockdata/mockActivities';
// import { managedActivities } from '../mockdata/mockActivities';
// import EditProfileModal from '../components/profile/EditProfileModal'; // 2. IMPORT MODAL

// const InfoRow = ({label, value, isBadge = false}) => (
//     <div className= "grid grid-cols-1 sm:grid-cols-[150px,1fr] items-center py-3 border-b border-gray-200">
//         <span className="font-semibold text-gray-600">{label}</span>
//         {isBadge ? (
//             <span className={`px-3 py-1 text-sm font-bold rounded-full w-fit ${value === 'ORGANIZER' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'}`}>
//                 {value}
//             </span>
//         ) : (
//             <span className="text-gray-800">{value}</span>
//         )}
//     </div>
// );

// const StatCard = ({ value, label, icon }) => (
//     <div className="bg-gray-50 p-4 rounded-lg flex items-center space-x-4 border border-gray-200">
//         <div className="text-3xl">{icon}</div>
//         <div>
//             <div className="text-2xl font-bold text-gray-800">{value}</div>
//             <div className="text-sm text-gray-500">{label}</div>
//         </div>
//     </div>
// );

// function ProfilePage({ user, setUser }) {
//     const navigate = useNavigate();
//     const [isEditModalOpen, setIsEditModalOpen] = useState(false);
//     const userStats = useMemo(() => {
//         if (!user) return null;

//         if (user.type === 'VOLUNTEER') {
//             const attendedActivities = myActivities.filter(act => act.status === 'completed-attended').length;
//             const totalDays = myActivities.reduce((sum, act) => {
//                 return act.status === 'completed-attended' ? sum + (act.recordedDays || 0) : sum;
//             }, 0);
//             return (
//                 <>
//                     <StatCard value={attendedActivities} label="Hoạt động đã tham gia" icon="✅" />
//                     <StatCard value={totalDays} label="Tổng ngày CTXH" icon="🗓️" />
//                     <StatCard value={myActivities.filter(act => act.status === 'pending').length} label="Hoạt động chờ duyệt" icon="⏳" />
//                 </>
//             );
//         }

//         if (user.type === 'ORGANIZER') {
//             return (
//                 <>
//                     <StatCard value={managedActivities.length} label="Hoạt động đang quản lý" icon="📋" />
//                     {/* Thêm các thống kê khác cho organizer nếu cần */}
//                 </>
//             );
//         }

//         return null;
//     }, [user]);


//     if (!user) {
//         return <div>Đang tải thông tin người dùng...</div>;
//     }
//     const handleSaveProfile = (updatedData) => {
//         console.log("Dữ liệu mới để lưu:", updatedData);

//         // Demo cập nhật state ở frontend
//         // Khi có API, bạn sẽ gọi API ở đây
//         const updatedUser = { ...user, ...updatedData };
//         setUser(updatedUser); // Cập nhật state ở App.jsx

//         alert("Hồ sơ đã được cập nhật! (Đây là demo)");
//         setIsEditModalOpen(false); // Đóng modal
//     };

//     return (
//         <>
//             <div className="mb-4">
//                 <button
//                     onClick={() => navigate(-1)}
//                     className="flex items-center text-gray-700 font-bold font-serif hover:text-blue-600 transition-colors duration-200"
//                 >
//                     <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
//                     Quay về
//                 </button>
//             </div>

//             {/* Phần thông tin cá nhân */}
//             <div className="bg-white p-4 sm:p-6 rounded-lg shadow-md border border-gray-200">
//                 <h1 className="text-2xl font-bold text-gray-800 mb-4 border-b pb-3">Hồ sơ cá nhân</h1>
//                 <div className="space-y-2">
//                     <InfoRow label="Tên hiển thị" value={user.display_name} />
//                     <InfoRow label="Email" value={user.email} />
//                     <InfoRow label="Vai trò" value={user.type} isBadge={true} />
//                 </div>
//                 <div className="mt-6 flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
//                     <button onClick={() => setIsEditModalOpen(true)} className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg">
//                         Chỉnh sửa hồ sơ
//                     </button>
//                     <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg">
//                         Đổi mật khẩu
//                     </button>
//                 </div>
//             </div>

//             {/* Phần thống kê */}
//             {userStats && (
//                 <div className="mt-8">
//                     <h2 className="text-xl font-bold text-gray-800 mb-4">Thống kê của bạn</h2>
//                     <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
//                         {userStats}
//                     </div>
//                 </div>
//             )}

//             <EditProfileModal
//                 isOpen={isEditModalOpen}
//                 onClose={() => setIsEditModalOpen(false)}
//                 user={user}
//                 onSave={handleSaveProfile}
//             />
//         </>
//     );
// }

// export default ProfilePage;


import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/apiClient';
import { useAuth } from '../context/AuthContext'; 
import EditProfileModal from '../components/profile/EditProfileModal';


const InfoRow = ({ label, value, isBadge = false }) => (
    <div className= "grid grid-cols-1 sm:grid-cols-[150px,1fr] items-center py-3 border-b border-gray-200">
        <span className="font-semibold text-gray-600">{label}</span>
        {isBadge ? (
            <span className={`px-3 py-1 text-sm font-bold rounded-full w-fit ${value === 'ORGANIZER' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'}`}>
                {value}
            </span>
        ) : (
            <span className="text-gray-800">{value}</span>
        )}
    </div>
);

const StatCard = ({ value, label, icon }) => (
    <div className="bg-gray-50 p-4 rounded-lg flex items-center space-x-4 border border-gray-200">
        <div className="text-3xl">{icon}</div>
        <div>
            <div className="text-2xl font-bold text-gray-800">{value}</div>
            <div className="text-sm text-gray-500">{label}</div>
        </div>
    </div>
);

function ProfilePage() {
    const { user, setUser } = useAuth();
    const navigate = useNavigate();

    const [isEditModalOpen, setIsEditModalOpen] = useState(false);

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProfile = async () => {
            if (user) {
                setIsLoading(false);
                return;
            }

            try {
                setIsLoading(true);
                const response = await apiClient.get('/users/profile/me');
                setUser(response.data);
            } catch (err) {
                setError("Không thể tải thông tin hồ sơ. Vui lòng thử lại.");
                console.error(err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchProfile();
    }, [user, setUser]); 


    const handleSaveProfile = async (updatedData) => {
        try {
            const response = await apiClient.patch('/users/profile/me', updatedData);
            setUser(response.data);
            alert("Hồ sơ đã được cập nhật thành công!");
            setIsEditModalOpen(false);
        } catch (err) {
            console.error("Failed to update profile:", err);
            alert(`Lỗi: ${err.response?.data?.detail || 'Không thể cập nhật hồ sơ.'}`);
        }
    };

    if (isLoading) return <div>Đang tải hồ sơ...</div>;
    if (error) return <div className="text-red-500">{error}</div>;
    if (!user) return <div>Không tìm thấy thông tin người dùng.</div>;

    const stats = user.stats || {};
    const userInfo = user.student_info || user.organizer_info || {};

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

            <div className="bg-white p-4 sm:p-6 rounded-lg shadow-md border border-gray-200">
                <h1 className="text-2xl font-bold text-gray-800 mb-4 border-b pb-3">Hồ sơ cá nhân</h1>
                <div className="space-y-2">
                    <InfoRow label="Tên đầy đủ" value={user.full_name || 'Chưa cập nhật'} />
                    <InfoRow label="Email" value={user.email} />
                    <InfoRow label="Số điện thoại" value={user.phone || 'Chưa cập nhật'} />
                    <InfoRow label="Mã số" value={userInfo.student_no || userInfo.organizer_no || 'N/A'} />
                    {user.type === 'ORGANIZER' && <InfoRow label="Tên tổ chức" value={userInfo.org_name || 'N/A'} />}
                    <InfoRow label="Vai trò" value={user.type} isBadge={true} />
                </div>
                <div className="mt-6 flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
                    <button onClick={() => setIsEditModalOpen(true)} className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg">Chỉnh sửa hồ sơ</button>
                </div>
            </div>

            <div className="mt-8">
                <h2 className="text-xl font-bold text-gray-800 mb-4">Thống kê của bạn</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {user.type === 'STUDENT' && (
                        <>
                            <StatCard value={stats.activities_joined || 0} label="Hoạt động đã tham gia" icon="✅" />
                            <StatCard value={stats.total_social_work_days || 0} label="Tổng ngày CTXH" icon="🗓️" />
                            <StatCard value={stats.pending_activities || 0} label="Hoạt động chờ duyệt" icon="⏳" />
                        </>
                    )}
                    {user.type === 'ORGANIZER' && (
                        <StatCard value={stats.managed_events_count || 0} label="Hoạt động đang quản lý" icon="📋" />
                    )}
                </div>
            </div>

            <EditProfileModal
                isOpen={isEditModalOpen}
                onClose={() => setIsEditModalOpen(false)}
                user={user}
                onSave={handleSaveProfile}
            />
        </>
    );
}

export default ProfilePage;