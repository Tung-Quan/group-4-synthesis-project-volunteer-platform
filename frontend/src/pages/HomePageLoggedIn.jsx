import React from 'react';
import Header from '../components/common/Header';
import WelcomeSection from '../components/home/WelcomeSection';
import SearchSection from '../components/home/SearchSection.jsx';
import RecentUpdates from '../components/home/RecentUpdates';
import Footer from '../components/common/Footer';

function HomePageLoggedIn({ navigateTo, onLogout, isLoggedIn, user , recentUpdates}) {
  return (
    <div className="min-h-screen bg-white-100 flex flex-col">
      <Header
        isLoggedIn={isLoggedIn}
        onLogout={onLogout}
        user={user}
        navigateTo={navigateTo}
      />
      
      <main className="flex-grow max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 w-full">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <WelcomeSection />
          <SearchSection navigateTo={navigateTo}/>
        </div>
        <RecentUpdates updates={recentUpdates} />
      </main>
      
      <Footer />
    </div>
  );
}

export default HomePageLoggedIn;