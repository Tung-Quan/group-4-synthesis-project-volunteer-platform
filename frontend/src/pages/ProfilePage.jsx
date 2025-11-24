import React, {useMemo} from "react";
import { useNavigate } from 'react-router-dom';
import { myActivities } from '../mockdata/mockActivities';
import { managedActivities } from '../mockdata/mockActivities';

const InfoRow = ({label, value, isBadge = false}) => (
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

function ProfilePage({ user }) {
    const navigate = useNavigate();

    // Sử dụng useMemo để tránh tính toán lại các thống kê không cần thiết
    const userStats = useMemo(() => {
        if (!user) return null;

        if (user.type === 'VOLUNTEER') {
            const attendedActivities = myActivities.filter(act => act.status === 'completed-attended').length;
            const totalDays = myActivities.reduce((sum, act) => {
                return act.status === 'completed-attended' ? sum + (act.recordedDays || 0) : sum;
            }, 0);
            return (
                <>
                    <StatCard value={attendedActivities} label="Hoạt động đã tham gia" icon="✅" />
                    <StatCard value={totalDays} label="Tổng ngày CTXH" icon="🗓️" />
                    <StatCard value={myActivities.filter(act => act.status === 'pending').length} label="Hoạt động chờ duyệt" icon="⏳" />
                </>
            );
        }

        if (user.type === 'ORGANIZER') {
            return (
                <>
                    <StatCard value={managedActivities.length} label="Hoạt động đang quản lý" icon="📋" />
                    {/* Thêm các thống kê khác cho organizer nếu cần */}
                </>
            );
        }

        return null;
    }, [user]);


    if (!user) {
        return <div>Đang tải thông tin người dùng...</div>;
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

            {/* Phần thông tin cá nhân */}
            <div className="bg-white p-4 sm:p-6 rounded-lg shadow-md border border-gray-200">
                <h1 className="text-2xl font-bold text-gray-800 mb-4 border-b pb-3">Hồ sơ cá nhân</h1>
                <div className="space-y-2">
                    <InfoRow label="Tên hiển thị" value={user.display_name} />
                    <InfoRow label="Email" value={user.email} />
                    <InfoRow label="Vai trò" value={user.type} isBadge={true} />
                </div>
                <div className="mt-6 flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
                    <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg">
                        Chỉnh sửa hồ sơ
                    </button>
                    <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg">
                        Đổi mật khẩu
                    </button>
                </div>
            </div>

            {/* Phần thống kê */}
            {userStats && (
                <div className="mt-8">
                    <h2 className="text-xl font-bold text-gray-800 mb-4">Thống kê của bạn</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {userStats}
                    </div>
                </div>
            )}
        </>
    );
}

export default ProfilePage;