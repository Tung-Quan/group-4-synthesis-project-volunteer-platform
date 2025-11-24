import React from 'react';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import ApplicationDetailHeader from '../components/application/ApplicationDetailHeader';
import { getUserDisplayName } from '../mockdata/mockUser';
import { useParams, useNavigate } from 'react-router-dom'; // 1. IMPORT
import { getApplication } from '../mockdata/mockApplications'; // Lấy hàm tìm đơn


function ApplicationDetailPage() {
  const handleAcceptClick = () => {
    console.log(`Đồng ý đơn ứng tuyển ID: ${selectedApplication.id}`);
    alert(`Bạn đã đồng ý cho "${getUserDisplayName(selectedApplication.volunteerId)}" tham gia hoạt động (Đây là demo).`);
  };

  const handleRejectClick = () => {
    console.log(`Từ chối đơn ứng tuyển ID: ${selectedApplication.id}`);
    alert(`Bạn đã từ chối cho "${getUserDisplayName(selectedApplication.volunteerId)}" tham gia hoạt động (Đây là demo).`);
  };
  const { appId } = useParams(); // 3. Lấy ID đơn từ URL
  const navigate = useNavigate();

  const selectedApplication = getApplication(appId); // 4. Tự tìm dữ liệu

  return (
    <>
        <div className="mb-6">
          <button 
             onClick={() => navigate(-1)}
            className="flex items-center text-gray-700 font-bold font-serif hover:text-blue-600 transition-colors duration-200"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Quay về
          </button>
        </div>
        
        <ApplicationDetailHeader 
          application={selectedApplication}
          onAcceptClick={handleAcceptClick}
		      onRejectClick={handleRejectClick}
        />

        <div className="bg-white p-6 mt-6 rounded-x1 shadow-md border border-gray-200">
          <div className="text-3xl font-serif font-bold text-gray-800 my-6">
			Nội dung đăng ký
		  </div>
          <hr className="my-4 border-gray-300" />
		  <div className="gap-x-2 py-1">
			<span className="text-gray-700 text-justify break-all">{selectedApplication.detail}</span>
		  </div>
        </div>
    </>
  );
}

export default ApplicationDetailPage;