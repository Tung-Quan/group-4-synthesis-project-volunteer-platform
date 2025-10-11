import React, { useState } from 'react';
import Header from './components/Header';
import PrimaryNavbar from './components/PrimaryNavBar';
import InfoCard from './components/InfoCard';
import ActivitySection from './components/ActivitySection';
import HeroImageSection from './components/HeroImageSection';
import CallToActionSection from './components/CallToActionSection';
import Footer from './components/Footer';
import LoginPage from './pages/LoginPage'; 

function App() {
  const [currentPage, setCurrentPage] = useState('home'); 

  const navigateTo = (page) => {
    setCurrentPage(page);
  };

  // Dữ liệu giả cho các hoạt động
  const currentActivities = [
    { title: "HỖ TRỢ CÔNG TÁC VĂN PHÒNG ĐOÀN TN - LIÊN CHI HỘI SV KHOA CƠ KHÍ TỪ NGÀY 15/9 ĐẾN 19/9/2025", location: "cơ sở 1, P. Diễn Hồng", date: "15/9-19/9/2025" },
    { title: "HỖ TRỢ BỘ MÔN KỸ THUẬT DỆT MAY ĐI DỜI MÁY 24.09.2025", location: "cơ sở 1, P. Diễn Hồng", date: "24/09/2025" },
    { title: "CÁC HOẠT ĐỘNG DI DỜI THIẾT BỊ VÀ DỌN DẸP PHÒNG THI NGHIỆM THUỘC KHOA CƠ KHÍ NGÀY 17.09.2025", location: "cơ sở 1, P. Diễn Hồng", date: "17/09/2025" },
    { title: "THAM GIA TỔ CHỨC LỄ ĐÓN TÂN SINH K2025 VÀ LỄ TRAO HỌC BỔNG KHOA CƠ KHÍ 05/9/2025", location: "cơ sở 1, P. Diễn Hồng", date: "05/09/2025" },
    { title: "GIAN HÀNG CHÀO ĐÓN TSV Khóa 2025", location: "Sân B1, CS1", date: "Khóa 2025" },
    { title: "Hoạt động thử nghiệm 1", location: "Địa điểm 1", date: "Ngày 1" },
    { title: "Hoạt động thử nghiệm 2", location: "Địa điểm 2", date: "Ngày 2" },
    { title: "Hoạt động thử nghiệm 3", location: "Địa điểm 3", date: "Ngày 3" },
  ];

  const newActivities = [
    { title: "[ĐD] ĐƠN DẸP NGHĨA TRANG LIỆT SĨ THÀNH PHỐ TUẦN 39/2025", location: "VRF6+7GR, Song Hành, Long Bình, Quận 9, Thành phố Hồ Chí Minh", date: "Tuần 39/2025" },
    { title: "[ĐD] ĐƠN DẸP LÀNG THIẾU NIÊN THỦ ĐỨC TUẦN 39/2025", location: "18 Đ. Võ Văn Ngân, Bình Thọ, Thủ Đức, Thành phố Hồ Chí Minh", date: "Tuần 39/2025" },
    { title: "[ĐD] HỖ TRỢ QUÁN CƠM MÁY NGÀN 1 TUẦN 39/2025", location: "239 Lý Thường Kiệt, phường 15, quận 11, TP. HCM", date: "Tuần 39/2025" },
    { title: "[ĐD] HỖ TRỢ QUÁN CƠM 2000 TUẦN 39/2025", location: "14/1 Ngô Quyền, Quận 10, TP.HCM", date: "Tuần 39/2025" },
    { title: "[HH] Chức danh sinh viên năm học 2024-2025 - K24", location: "cơ sở 2", date: "2024-2025" },
    { title: "Hoạt động mới thử nghiệm 1", location: "Địa điểm mới 1", date: "Ngày mới 1" },
    { title: "Hoạt động mới thử nghiệm 2", location: "Địa điểm mới 2", date: "Ngày mới 2" },
  ];

  // Component HomePageContent để chứa tất cả nội dung trang chủ
  const HomePageContent = () => (
    <div className="min-h-screen bg-rose-50 flex flex-col">
      <Header onLoginClick={navigateTo} hideLoginButton={currentPage === 'login'} />
      <PrimaryNavbar currentPage={currentPage} navigateTo={navigateTo} />

      <main className="flex-grow max-w-7xl mx-auto p-4 md:flex md:space-x-8 lg:space-x-12 mt-6">
        {/* Left Column */}
        <div className="w-full md:w-1/2 lg:w-2/5 space-y-8 mb-8 md:mb-0">
          <div className="space-y-4">
            <InfoCard icon="🔍" title="Dễ dàng tìm kiếm" description="Tìm kiếm các hoạt động phù hợp với sở thích của bạn." />
            <InfoCard icon="✍️" title="Đăng ký tham gia" description="Tham gia nhanh chóng chỉ với vài cú nhấp chuột." />
            <InfoCard icon="🏅" title="Tích lũy ngày CTXH" description="Theo dõi và tích lũy thời gian hoạt động công tác xã hội." />
          </div>
          <HeroImageSection />
        </div>

        
        <div className="w-full md:w-1/2 lg:w-3/5 space-y-6">
          <ActivitySection title="Các hoạt động đang diễn ra" activities={currentActivities} />
          <ActivitySection title="Các hoạt động mới" activities={newActivities} />
        </div>
      </main>

      <CallToActionSection onLoginClick={navigateTo} />
      <Footer />
    </div>
  );

  return (
    <>
      {currentPage === 'home' && <HomePageContent />}
      {currentPage === 'login' && <LoginPage navigateTo={navigateTo} />}
    </>
  );
}

export default App;
