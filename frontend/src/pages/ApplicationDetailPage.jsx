import React from 'react';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import ApplicationDetailHeader from '../components/application/ApplicationDetailHeader';
import { getUserDisplayName } from '../mockdata/mockUser';

function ApplicationDetailPage({ navigateTo, onLogout, isLoggedIn, user, application, previousPage }) {
  const handleAcceptClick = () => {
    console.log(`Đồng ý đơn ứng tuyển ID: ${application.id}`);
    alert(`Bạn đã đồng ý cho "${getUserDisplayName(application.volunteerId)}" tham gia hoạt động (Đây là demo).`);
  };

  const handleRejectClick = () => {
    console.log(`Từ chối đơn ứng tuyển ID: ${application.id}`);
    alert(`Bạn đã từ chối cho "${getUserDisplayName(application.volunteerId)}" tham gia hoạt động (Đây là demo).`);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <Header
        isLoggedIn={isLoggedIn}	
        onLogout={onLogout}
        user={user}
        navigateTo={navigateTo}
      />
      
      <main className="flex-grow max-w-5xl mx-auto p-4 sm:p-6 lg:p-8 w-full">
        <div className="mb-6">
          <button 
             onClick={() => navigateTo(previousPage || 'home-logged-in')}
            className="flex items-center text-gray-700 font-bold font-serif hover:text-blue-600 transition-colors duration-200"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Quay về
          </button>
        </div>
        
        <ApplicationDetailHeader 
          application={application}
          onAcceptClick={handleAcceptClick}
		      onRejectClick={handleRejectClick}
        />

        <div className="bg-white p-6 mt-6 rounded-x1 shadow-md border border-gray-200">
          <div className="text-3xl font-serif font-bold text-gray-800 my-6">
			Nội dung đăng ký
		  </div>
          <hr className="my-4 border-gray-300" />
		  <div className="gap-x-2 py-1">
			<span className="text-gray-700 text-justify break-all">{application.detail}</span>
		  </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default ApplicationDetailPage;