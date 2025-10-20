import React from 'react';
import Header from '../components/common/Header';
import HeroImage from '../components/HeroImage';
import AboutAndCTASection from '../components/common/AboutAndCTASection.jsx';
import Footer from '../components/common/Footer';

function HomePageLoggedOut({ navigateTo, isLoggedIn }) {
  return (
    <div className="min-h-screen bg-white-100 flex flex-col">
      <Header navigateTo = {navigateTo} isLoggedIn={isLoggedIn} />

      <main className="flex-grow">
        <HeroImage />
        <AboutAndCTASection navigateTo={navigateTo} />
      </main>

      <Footer />
    </div>
  );
}

export default HomePageLoggedOut;