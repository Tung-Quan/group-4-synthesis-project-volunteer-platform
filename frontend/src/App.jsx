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
import CreateNewActivityPage from './pages/CreateNewActivityPage';

// Import Helpers
import ProtectedRoute from './components/common/ProtectedRoute';
import MainLayout from './components/common/MainLayout';

function App() {
  const { isLoggedIn, user, setUser, isLoading } = useAuth();
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
      {/* === PUBLIC ROUTES === */}
      <Route path="/guest" element={<HomePageLoggedOut navigateTo={navigate} />} />
      <Route path="/login" element={<LoginPage />} />

      {/* === PRIVATE ROUTES (sử dụng layout và được bảo vệ) === */}
      <Route 
        path="/" 
        element={
          <ProtectedRoute isLoggedIn={isLoggedIn} user={user}>
            <MainLayout 
            />
          </ProtectedRoute>
        }
      >
        
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
          path="organizer/activities/new" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER']}>
              <CreateNewActivityPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="organizer/dashboard/:activityId" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER']}>
              <ActivityDetailDashboard />
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

      <Route path="*" element={<Navigate to={isLoggedIn ? "/" : "/guest"} replace />} />
    </Routes>
  );
}

export default App;