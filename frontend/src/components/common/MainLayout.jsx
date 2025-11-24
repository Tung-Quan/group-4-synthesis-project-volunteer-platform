import React from 'react';
import Header from './Header';
import Footer from './Footer';
import { Outlet } from 'react-router-dom';

function MainLayout({ isLoggedIn, user, onLogout }) {
    return (
        <div className="min-h-screen bg-gray-100 flex flex-col">
            <Header
                isLoggedIn={isLoggedIn}
                user={user}
                onLogout={onLogout}
            />

            <main className="flex-grow w-full max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
                {/* Outlet là nơi các component trang con sẽ được render */}
                <Outlet />
            </main>

            <Footer />
        </div>
    );
}

export default MainLayout;