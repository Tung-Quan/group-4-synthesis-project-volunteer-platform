import React from 'react';
import Header from '../components/common/Header';
import WelcomeSection from '../components/home/WelcomeSection';
import SearchSection from '../components/home/SearchSection.jsx';
import RecentUpdates from '../components/home/RecentUpdates';
import Footer from '../components/common/Footer';
import { recentUpdates } from '../mockdata/mockActivities'; // 1. IMPORT DỮ LIỆU Ở ĐÂY


function HomePageLoggedIn({ navigateTo}) {
  return (
    <>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <WelcomeSection />
          <SearchSection navigateTo={navigateTo}/>
        </div>
        <RecentUpdates updates={recentUpdates} />
    </>
    );
}

export default HomePageLoggedIn;