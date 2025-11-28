// import React, { useState } from 'react';
// import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';

// import HomePageLoggedOut from './pages/HomePageLoggedOut'; 
// import HomePageLoggedIn from './pages/HomePageLoggedIn'; 
// import LoginPage from './pages/LoginPage';
// import NewActivitiesPage from './pages/NewActivitiesPage';
// import CurrentActivitiesPage from './pages/CurrentActivitiesPage'; 
// import ActivityDetailPage from './pages/ActivityDetailPage';
// import ApplicationReviewPage from './pages/ApplicationReviewPage';
// import ApplicationDetailPage from './pages/ApplicationDetailPage';
// import ParticipatingPage from './pages/ParticipatingPage.jsx';
// import HistoryPage from './pages/HistoryPage';

// import { 
//   recentUpdates,
// } from './mockdata/mockActivities.js';

// import SearchResultsPage from './pages/SearchResultsPage.jsx';
// import ActivityDashboard from './pages/ActivityDashboard.jsx';
// import ActivityDetailDashboard from './pages/ActivityDetailDashboard.jsx';


// import ProtectedRoute from './components/common/ProtectedRoute.jsx'; 

// function App() {
//   // const [currentPage, setCurrentPage] = useState('home-logged-out'); 
//   // const [currentActivityId, setCurrentActivityId] = useState(null);
//   // const [currentApplicationId, setCurrentApplicationId] = useState(null);
//   // const [previousPage, setPreviousPage] = useState(null);
//   // const [searchQuery, setSearchQuery] = useState(''); // State cho từ khóa tìm kiếm
//   // const [redirectAfterLogin, setRedirectAfterLogin] = useState(null); // State để lưu trang cần chuyển đến sau khi login
//   // const organizerOnlyPages = ['application-review', 'activity-dashboard', 'activity-detail-dashboard'];

//   const [isLoggedIn, setIsLoggedIn] = useState(false); // Trạng thái đăng nhập
//   const [user, setUser] = useState(null);

//   const navigate = useNavigate();
//   const location = useLocation();

//   // const navigateTo = (page, params = {}) => {
//   //   setPreviousPage(currentPage);
//   //   if (page === 'login' && params.redirectAfterLogin) {
//   //     setRedirectAfterLogin(params.redirectAfterLogin);
//   //   } 
//   //   setCurrentPage(page);
//   //   if (page === 'activity-detail' && params.id) {
//   //     setCurrentActivityId(params.id);
//   //   }
//   //   if (page === 'application-detail' && params.id) {
//   //     setCurrentApplicationId(params.id);
//   //   }
//   //   if (page === 'search-results' && params.query) {
//   //     setSearchQuery(params.query);
//   //   }
//   // };

//   const handleLoginSuccess = (loggedInUser) => {
//     setIsLoggedIn(true);
//     setUser(loggedInUser);
//     const from = location.state?.from?.pathname || '/'; // lấy trang đang định chuyển hướng hoặc về trang chủ
//     navigate(from, { replace: true });
//   };

//   const handleLogout = () => {
//     setIsLoggedIn(false);
//     setUser(null);
//     navigate('/home-logged-out'); 
//   };

//   // const selectedActivity = allActivitiesDetails[currentActivityId];
//   // const selectedApplication = getApplication(currentApplicationId);
//   // // TÌM TRẠNG THÁI ĐĂNG KÝ CỦA NGƯỜI DÙNG CHO HOẠT ĐỘNG ĐANG XEM
//   // const userApplicationStatus = myActivities.find(
//   //   activity => activity.id === currentActivityId
//   // )?.status || null; // Dùng ?. (optional chaining) để an toàn

// //   return (
// //     <>
// //       {/* HomePageLoggedOut*/}
// //       {currentPage === 'home-logged-out' && (
// //         <HomePageLoggedOut
// //           navigateTo={navigateTo}
// //           isLoggedIn={isLoggedIn}
// //         />
// //       )}

// //       {/*LoginPage*/}
// //       {currentPage === 'login' && (
// //         <LoginPage
// //           navigateTo={navigateTo}
// //           onLoginSuccess={handleLoginSuccess}
// //           isLoggedIn={isLoggedIn}
// //         />
// //       )}

// //       {/* HomePageLoggedIn*/}
// //       {isLoggedIn && (currentPage === 'home-logged-in') && (
// //         <HomePageLoggedIn
// //           navigateTo={navigateTo}
// //           onLogout={handleLogout}
// //           isLoggedIn={isLoggedIn}
// //           user={user} 
// //           recentUpdates={recentUpdates}
// //         />
// //       )}

// //       {/* Trang kết quả tìm kiếm */}
// //       {isLoggedIn && currentPage === 'search-results' && (
// //         <SearchResultsPage
// //           navigateTo={navigateTo}
// //           onLogout={handleLogout}
// //           isLoggedIn={isLoggedIn}
// //           user={user}
// //           searchQuery={searchQuery}
// //         />
// //       )}

// //       {/* Trang Hoạt động mới */}
// //       {isLoggedIn && currentPage === 'new-activities' && (
// //         <NewActivitiesPage
// //           navigateTo={navigateTo}
// //           onLogout={handleLogout}
// //           isLoggedIn={isLoggedIn}
// //           user={user}
// //           activities={newActivities}
// //         />
// //       )}

// //       {/* Trang Hoạt động đang diễn ra */}
// //       {isLoggedIn && currentPage === 'current-activities' && (
// //         <CurrentActivitiesPage
// //           navigateTo={navigateTo}
// //           onLogout={handleLogout}
// //           isLoggedIn={isLoggedIn}
// //           user={user}
// //           activities={currentActivities}
// //         />
// //       )}

// //       {/* Trang Chi tiết Hoạt động */}
// //       {isLoggedIn && currentPage === 'activity-detail' && selectedActivity && (
// //         <ActivityDetailPage
// //           navigateTo={navigateTo}
// //           onLogout={handleLogout}
// //           isLoggedIn={isLoggedIn}
// //           user={user}
// //           activity={selectedActivity}
// //           previousPage={previousPage}
// //           applicationStatus={userApplicationStatus}
// //         />
// //       )}

// //       {isLoggedIn && currentPage === 'participating-activities' && (
// //         <ParticipatingPage
// //           navigateTo={navigateTo}
// //           onLogout={handleLogout}
// //           isLoggedIn={isLoggedIn}
// //           user={user}
// //         />
// //       )}

// //       {isLoggedIn && currentPage === 'history-activities' && (
// //         <HistoryPage
// //           navigateTo={navigateTo}
// //           onLogout={handleLogout}
// //           isLoggedIn={isLoggedIn}
// //           user={user}
// //         />
// //       )}
      
// //       {/* Trang duyệt đơn ứng tuyển của organizer */}
// //       {isLoggedIn && currentPage === 'application-review' && (
// //         <ApplicationReviewPage
// //           navigateTo={navigateTo}
// //           onLogout={handleLogout}
// //           isLoggedIn={isLoggedIn}
// //           user={user}
// //           applications={applicationDetails}
// //         />
// //       )}

// //       {/* Trang Chi tiết đơn ứng tuyển */}
// //       {isLoggedIn && currentPage === 'application-detail' && (
// //         <ApplicationDetailPage
// //           navigateTo={navigateTo}
// //           onLogout={handleLogout}
// //           isLoggedIn={isLoggedIn}
// //           user={user}
// //           application={selectedApplication}
// //           previousPage={previousPage}
// //         />
// //       )}

      
// //       {/* Trang quản lý các hoạt động của organizer */}
// //       {isLoggedIn && currentPage === 'activity-dashboard' && (
// //         <ActivityDashboard
// //           navigateTo={navigateTo}
// //           onLogout={handleLogout}
// //           isLoggedIn={isLoggedIn}
// //           user={user}
// //           activities={managedActivities}
// //         />
// //       )}
// //       {isLoggedIn && currentPage === 'activity-detail-dashboard' && selectedActivity && (
// //         <ActivityDetailDashboard
// //           navigateTo={navigateTo}
// //           onLogout={handleLogout}
// //           isLoggedIn={isLoggedIn}
// //           user={user}
// //           activity={selectedActivity}
// //           previousPage={previousPage}
// //         />
// //       )}

// //     </>
// //   );
// // }

// // export default App;

// return (
//   <Routes>
//     <Route
//       path="/home-logged-out"
//       element={<HomePageLoggedOut navigateTo={navigate} />}
//     />
//     <Route
//     path="/login"
//     element={<LoginPage onLoginSuccess={handleLoginSuccess} navigateTo={navigate} />}
//     />

//     {/*trang chủ*/}
//     <Route
//       path="/"
//       element={
//         isLoggedIn
//           ? <HomePageLoggedIn onLogout={handleLogout} user={user} navigateTo={navigate} recentUpdates={recentUpdates} />
//           : <HomePageLoggedOut navigateTo={navigate} />
//       }
//     />

//     {/* --- CÁC ROUTE CHUNG (Cả VOLUNTEER & ORGANIZER đều xem được) --- */}
//     <Route path="/search" element={
//       <ProtectedRoute isLoggedIn={isLoggedIn} user={user}>
//         <SearchResultsPage onLogout={handleLogout} user={user} navigateTo={navigate} />
//       </ProtectedRoute>
//     } />
//     <Route path="/activities/new" element={
//       <ProtectedRoute isLoggedIn={isLoggedIn} user={user}>
//         <NewActivitiesPage onLogout={handleLogout} user={user} navigateTo={navigate} />
//       </ProtectedRoute>
//     } />
//     <Route path="/activities/current" element={
//       <ProtectedRoute isLoggedIn={isLoggedIn} user={user}>
//         <CurrentActivitiesPage onLogout={handleLogout} user={user} navigateTo={navigate} />
//       </ProtectedRoute>
//     } />

//     {/* Route với tham số động */}
//     <Route path="/activities/:activityId" element={
//       <ProtectedRoute isLoggedIn={isLoggedIn} user={user}>
//         <ActivityDetailPage onLogout={handleLogout} user={user} />
//       </ProtectedRoute>
//     } />

//     {/* --- CÁC ROUTE CHỈ DÀNH CHO VOLUNTEER --- */}
//     <Route path="/participating" element={
//       <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['VOLUNTEER', 'BOTH']}>
//         <ParticipatingPage onLogout={handleLogout} user={user} navigateTo={navigate} />
//       </ProtectedRoute>
//     } />
//     <Route path="/history" element={
//       <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['VOLUNTEER', 'BOTH']}>
//         <HistoryPage onLogout={handleLogout} user={user} navigateTo={navigate} />
//       </ProtectedRoute>
//     } />

//     {/* --- CÁC ROUTE CHỈ DÀNH CHO ORGANIZER --- */}
//     <Route path="/organizer/dashboard" element={
//       <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER', 'BOTH']}>
//         <ActivityDashboard onLogout={handleLogout} user={user} navigateTo={navigate} />
//       </ProtectedRoute>
//     } />
//     <Route path="/organizer/dashboard/:activityId" element={
//       <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER', 'BOTH']}>
//         <ActivityDetailDashboard onLogout={handleLogout} user={user} />
//       </ProtectedRoute>
//     } />
//     <Route path="/organizer/applications" element={
//       <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER', 'BOTH']}>
//         <ApplicationReviewPage onLogout={handleLogout} user={user} navigateTo={navigate} />
//       </ProtectedRoute>
//     } />
//     <Route path="/organizer/applications/:appId" element={
//       <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER', 'BOTH']}>
//         <ApplicationDetailPage onLogout={handleLogout} user={user} />
//       </ProtectedRoute>
//     } />

//     <Route path="*" element={
//       isLoggedIn
//         ? <HomePageLoggedIn onLogout={handleLogout} user={user} navigateTo={navigate} recentUpdates={recentUpdates} />
//         : <HomePageLoggedOut navigateTo={navigate} />
//     } />

//   </Routes>
//   );
// }

// export default App;

import React from 'react';
import { Routes, Route, useNavigate, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';

import HomePageLoggedOut from './pages/HomePageLoggedOut';
import LoginPage from './pages/LoginPage';
import HomePageLoggedIn from './pages/HomePageLoggedIn';
import NewActivitiesPage from './pages/NewActivitiesPage';
import CurrentActivitiesPage from './pages/CurrentActivitiesPage';
import ActivityDetailPage from './pages/ActivityDetailPage';
import SearchResultsPage from './pages/SearchResultsPage';
import ParticipatingPage from './pages/ParticipatingPage';
import HistoryPage from './pages/HistoryPage';
import ProfilePage from './pages/ProfilePage';
// Organizer Pages
import ActivityDashboard from './pages/ActivityDashboard';
import ActivityDetailDashboard from './pages/ActivityDetailDashboard';
import ApplicationReviewPage from './pages/ApplicationReviewPage';
import ApplicationDetailPage from './pages/ApplicationDetailPage';

// Import Helpers
import ProtectedRoute from './components/common/ProtectedRoute';
import MainLayout from './components/common/MainLayout';

function App() {
  const { isLoggedIn, user, setUser, logout, isLoading } = useAuth();
  const navigate = useNavigate();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl font-semibold">Đang tải ứng dụng...</div>
      </div>
    );
  }

  return (
    <Routes>
      {/* === PUBLIC ROUTES (không dùng layout) === */}
      <Route path="/home-logged-out" element={<HomePageLoggedOut navigateTo={navigate} />} />
      <Route path="/login" element={<LoginPage />} />

      {/* === PRIVATE ROUTES (sử dụng layout và được bảo vệ) === */}
      <Route 
        path="/" 
        element={
          <ProtectedRoute isLoggedIn={isLoggedIn} user={user}>
            <MainLayout isLoggedIn={isLoggedIn} user={user} onLogout={logout} />
          </ProtectedRoute>
        }
      >
        {/* 2. Các route con (nested) sẽ được render bên trong <Outlet /> của MainLayout */}
        
        {/* Route mặc định (trang chủ) */}
        <Route index element={<HomePageLoggedIn />} />

        {/* --- Routes chung --- */}
        <Route path="search" element={<SearchResultsPage />} />
        <Route path="profile" element={<ProfilePage user={user} setUser={setUser} />} />
        <Route path="activities/new" element={<NewActivitiesPage />} />
        <Route path="activities/current" element={<CurrentActivitiesPage />} />
        <Route path="activities/:activityId" element={<ActivityDetailPage user={user} />} />

        {/* --- Routes của Volunteer --- */}
        <Route 
          path="participating" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['STUDENT']}>
              <ParticipatingPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="history" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['STUDENT']}>
              <HistoryPage />
            </ProtectedRoute>
          } 
        />

        {/* --- Routes của Organizer --- */}
        <Route 
          path="organizer/dashboard" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER']}>
              <ActivityDashboard />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="organizer/dashboard/:activityId" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER']}>
              <ActivityDetailDashboard user={user} />
            </ProtectedRoute>
          }
        />
        <Route 
          path="organizer/applications" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER']}>
              <ApplicationReviewPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="organizer/applications/:appId" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER']}>
              <ApplicationDetailPage user={user} />
            </ProtectedRoute>
          } 
        />
      </Route>

      <Route path="*" element={<Navigate to={isLoggedIn ? "/" : "/home-logged-out"} replace />} />
    </Routes>
  );
}

export default App;