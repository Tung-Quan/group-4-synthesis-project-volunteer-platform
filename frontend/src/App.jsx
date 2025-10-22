import React, { useState } from 'react';
import HomePageLoggedOut from './pages/HomePageLoggedOut'; 
import HomePageLoggedIn from './pages/HomePageLoggedIn'; 
import LoginPage from './pages/LoginPage';

import NewActivitiesPage from './pages/NewActivitiesPage';
import CurrentActivitiesPage from './pages/CurrentActivitiesPage'; 
import ActivityDetailPage from './pages/ActivityDetailPage';
import ApplicationReviewPage from './pages/ApplicationReviewPage';
import ApplicationDetailPage from './pages/ApplicationDetailPage';
 
import { 
  allActivitiesDetails, 
  newActivities, 
  currentActivities,
  recentUpdates,
  managedActivities,
} from './mockdata/mockActivities.js';

import SearchResultsPage from './pages/SearchResultsPage.jsx';
import { applicationDetails, getApplication } from './mockdata/mockApplications.js';
import ActivityDashboard from './pages/ActivityDashboard.jsx';
import ActivityDetailDashboard from './pages/ActivityDetailDashboard.jsx';



function App() {
  const [currentPage, setCurrentPage] = useState('home-logged-out'); 
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Trạng thái đăng nhập
  const [currentActivityId, setCurrentActivityId] = useState(null);
  const [currentApplicationId, setCurrentApplicationId] = useState(null);
  const [previousPage, setPreviousPage] = useState(null);
  const [user, setUser] = useState(null);
  const [searchQuery, setSearchQuery] = useState(''); // State cho từ khóa tìm kiếm
  const [redirectAfterLogin, setRedirectAfterLogin] = useState(null); // State để lưu trang cần chuyển đến sau khi login


  const navigateTo = (page, params = {}) => {
    setPreviousPage(currentPage);
    if (page === 'login' && params.redirectAfterLogin) {
      setRedirectAfterLogin(params.redirectAfterLogin);
    } 
    setCurrentPage(page);
    if (page === 'activity-detail' && params.id) {
      setCurrentActivityId(params.id);
    }
    if (page === 'application-detail' && params.id) {
      setCurrentApplicationId(params.id);
    }
    if (page === 'search-results' && params.query) {
      setSearchQuery(params.query);
    }
  };

  const handleLoginSuccess = (loggedInUser) => {
    setIsLoggedIn(true);
    setUser(loggedInUser);
    setCurrentPage(redirectAfterLogin || 'home-logged-in');
    setRedirectAfterLogin(null);
};

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
    setCurrentPage('home-logged-out');
    setRedirectAfterLogin(null); 
  };

  const selectedActivity = allActivitiesDetails[currentActivityId];
  const selectedApplication = getApplication(currentApplicationId);

  return (
    <>
      {/* HomePageLoggedOut*/}
      {currentPage === 'home-logged-out' && (
        <HomePageLoggedOut
          navigateTo={navigateTo}
          isLoggedIn={isLoggedIn}
        />
      )}

      {/*LoginPage*/}
      {currentPage === 'login' && (
        <LoginPage
          navigateTo={navigateTo}
          onLoginSuccess={handleLoginSuccess}
          isLoggedIn={isLoggedIn}
        />
      )}

      {/* HomePageLoggedIn*/}
      {isLoggedIn && (currentPage === 'home-logged-in') && (
        <HomePageLoggedIn
          navigateTo={navigateTo}
          onLogout={handleLogout}
          isLoggedIn={isLoggedIn}
          user={user} 
          recentUpdates={recentUpdates}
        />
      )}

      {/* Trang kết quả tìm kiếm */}
      {isLoggedIn && currentPage === 'search-results' && (
        <SearchResultsPage
          navigateTo={navigateTo}
          onLogout={handleLogout}
          isLoggedIn={isLoggedIn}
          user={user}
          searchQuery={searchQuery}
        />
      )}

      {/* Trang Hoạt động mới */}
      {isLoggedIn && currentPage === 'new-activities' && (
        <NewActivitiesPage
          navigateTo={navigateTo}
          onLogout={handleLogout}
          isLoggedIn={isLoggedIn}
          user={user}
          activities={newActivities}
        />
      )}

      {/* Trang Hoạt động đang diễn ra */}
      {isLoggedIn && currentPage === 'current-activities' && (
        <CurrentActivitiesPage
          navigateTo={navigateTo}
          onLogout={handleLogout}
          isLoggedIn={isLoggedIn}
          user={user}
          activities={currentActivities}
        />
      )}

      {/* Trang Chi tiết Hoạt động */}
      {isLoggedIn && currentPage === 'activity-detail' && selectedActivity && (
        <ActivityDetailPage
          navigateTo={navigateTo}
          onLogout={handleLogout}
          isLoggedIn={isLoggedIn}
          user={user}
          activity={selectedActivity}
          previousPage={previousPage}
        />
      )}

      {/* Trang duyệt đơn ứng tuyển của organizer */}
      {isLoggedIn && currentPage === 'application-review' && (
        <ApplicationReviewPage
          navigateTo={navigateTo}
          onLogout={handleLogout}
          isLoggedIn={isLoggedIn}
          user={user}
          applications={applicationDetails}
        />
      )}

      {/* Trang Chi tiết đơn ứng tuyển */}
      {isLoggedIn && currentPage === 'application-detail' && (
        <ApplicationDetailPage
          navigateTo={navigateTo}
          onLogout={handleLogout}
          isLoggedIn={isLoggedIn}
          user={user}
          application={selectedApplication}
          previousPage={previousPage}
        />
      )}

      
      {/* Trang quản lý các hoạt động của organizer */}
      {isLoggedIn && currentPage === 'activity-dashboard' && (
        <ActivityDashboard
          navigateTo={navigateTo}
          onLogout={handleLogout}
          isLoggedIn={isLoggedIn}
          user={user}
          activities={managedActivities}
        />
      )}
      {isLoggedIn && currentPage === 'activity-detail-dashboard' && selectedActivity && (
        <ActivityDetailDashboard
          navigateTo={navigateTo}
          onLogout={handleLogout}
          isLoggedIn={isLoggedIn}
          user={user}
          activity={selectedActivity}
          previousPage={previousPage}
        />
      )}

    </>
  );
}

export default App;