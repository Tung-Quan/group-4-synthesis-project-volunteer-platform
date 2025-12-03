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
import SeeAppOfEventPage from './pages/SeeAppOfEventPage';
import CreateNewActivityPage from './pages/CreateNewActivityPage';
import SeeAppInSlotPage from './pages/SeeAppInSlotPage';
import ActivityEditor from './pages/ActivityEditor';
import CheckAttendance from './pages/CheckAttendance';

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
      <Route path="/guest" element={<HomePageLoggedOut navigateTo={navigate} />} />
      <Route path="/login" element={<LoginPage />} />

      <Route 
        path="/" 
        element={
          <ProtectedRoute isLoggedIn={isLoggedIn} user={user}>
            <MainLayout 
            />
          </ProtectedRoute>
        }
      >
        
        <Route index element={<HomePageLoggedIn />} />

        <Route path="search" element={<SearchResultsPage />} />
        <Route path="profile" element={<ProfilePage user={user} setUser={setUser} />} />
        <Route path="activities/new" element={<NewActivitiesPage />} />
        <Route path="activities/current" element={<CurrentActivitiesPage />} />
        <Route path="activities/:activityId" element={<ActivityDetailPage user={user} />} />

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
              <ActivityDetailDashboard user={user}/>
            </ProtectedRoute>
          }
        />
        <Route 
          path="organizer/dashboard/:activityId/edit" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER']}>
              <ActivityEditor user={user} />
            </ProtectedRoute>
          }
        />
        <Route 
          path="organizer/dashboard/:activityId/:slotId/attendance" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER']}>
              <CheckAttendance user={user} />
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
          path="organizer/applications/:activityId" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER']}>
              <SeeAppOfEventPage user={user} />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="organizer/applications/:activityId/:slotId" 
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn} user={user} allowedRoles={['ORGANIZER']}>
              <SeeAppInSlotPage user={user} />
            </ProtectedRoute>
          } 
        />
      </Route>

      <Route path="*" element={<Navigate to={isLoggedIn ? "/" : "/guest"} replace />} />
    </Routes>
  );
}

export default App;