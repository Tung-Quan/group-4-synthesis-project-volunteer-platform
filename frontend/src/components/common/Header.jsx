import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import DropdownMenu from './DropdownMenu.jsx';
import { useAuth } from '../../context/AuthContext'; 


function Header({ isLoginPage = false }) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const { isLoggedIn, user, logout } = useAuth();
  
  const volunteerMenuItems = ['Hoạt động đang tham gia', 'Lịch sử tham gia'];
  const activityMenuItems = ['Hoạt động đang diễn ra', 'Hoạt động mới'];
  const userMenuItems = ['Hồ sơ', 'Đăng xuất'];
  const organizerMenuItems = ['Duyệt đơn đăng kí', 'Quản lý hoạt động'];
  const guestPersonalMenuItems = [...volunteerMenuItems, ...organizerMenuItems];

  const handleUserMenuClick = (item) => {
    if (item === 'Đăng xuất') {
      logout(navigate);
    }
    if(item ==="Hồ sơ"){
      navigate('/profile');
    }
    setIsMobileMenuOpen(false);
  };

  const handlePersonalMenuClick = (item) => {
    let targetPage = null;
    if (item === 'Hoạt động đang tham gia') targetPage = '/participating';
    if (item === 'Lịch sử tham gia') targetPage = '/history';
    if (item === 'Duyệt đơn đăng kí') targetPage = '/organizer/applications';
    if (item === 'Quản lý hoạt động') targetPage = '/organizer/dashboard';

    if (targetPage) {
      if (isLoggedIn) {
        navigate(targetPage);
      } else {
        navigate('/login', { state: { from: { pathname: targetPage } } });
      }
    }
    setIsMobileMenuOpen(false);
  };

  const handleActivityMenuClick = (item) => {
    let targetPage = null;
    if (item === 'Hoạt động mới') targetPage = '/activities/new';
    if (item === 'Hoạt động đang diễn ra') targetPage = '/activities/current';

    if (targetPage) {
      if (isLoggedIn) {
        navigate(targetPage);
      } else {
        navigate('/login', { state: { from: { pathname: targetPage } } });
      }
    }
    setIsMobileMenuOpen(false);
  };

  const handleLoginButtonClick = () => {
    navigate('/login');
    setIsMobileMenuOpen(false);
  };

  
  return (
    <header className="bg-blue-700 px-4 sm:px-6 py-3 flex items-center justify-between shadow-lg h-16 relative">
      <Link to={isLoggedIn ? "/" : "/guest"} className="flex items-center">
        <img src="/icon.svg" alt="Bach Khoa Logo" className="h-10 w-auto mr-3" />
        <h1 className="text-xl md:text-2xl font-extrabold text-white" style={{ textShadow: '0 0 2px black, 0 0 2px black, 0 0 2px black, 0 0 2px black' }}>
          Bach Khoa Volunteer Hub
        </h1>
      </Link>

      {/* --- PHẦN DESKTOP --- */}
      <div className="hidden md:flex items-center space-x-4">
        {isLoggedIn && user ? (
          // Menu khi đã đăng nhập
          <>
            <DropdownMenu title={user.type === 'STUDENT' ? 'Cá nhân' : 'Quản lý'} items={user.type === 'STUDENT' ? volunteerMenuItems : organizerMenuItems} onMenuItemClick={handlePersonalMenuClick} />
            <DropdownMenu title="Hoạt động" items={activityMenuItems} onMenuItemClick={handleActivityMenuClick} />
            <DropdownMenu title={user.full_name || user.email} items={userMenuItems} onMenuItemClick={handleUserMenuClick} />
          </>
        ) : (
          // Menu khi CHƯA đăng nhập
          !isLoginPage && (
            <>
              <DropdownMenu title="Cá nhân" items={guestPersonalMenuItems} onMenuItemClick={handlePersonalMenuClick} />
              <DropdownMenu title="Hoạt động" items={activityMenuItems} onMenuItemClick={handleActivityMenuClick} />
              <button
                onClick={handleLoginButtonClick}
                className="bg-white text-blue-700 font-bold text-sm py-1.5 px-4 rounded-lg flex items-center transition-colors duration-200 hover:bg-gray-200"
              >
                <span className="mr-1.5 text-base">👤</span> Đăng nhập
              </button>
            </>
          )
        )}
      </div>

      {/* --- PHẦN MOBILE --- (Logic tương tự phần Desktop) */}
      {!isLoginPage && (
        <div className="md:hidden">
          <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="text-white focus:outline-none">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-8 6h8"></path>
            </svg>
          </button>
        </div>
      )}

      {isMobileMenuOpen && !isLoginPage && (
        <div className="md:hidden absolute top-16 left-0 w-full bg-blue-800 shadow-lg z-20">
          <div className="flex flex-col items-center space-y-4 py-4">
            {isLoggedIn && user ? (
              <>
                <DropdownMenu title={user.type === 'STUDENT' ? 'Cá nhân' : 'Quản lý'} items={user.type === 'STUDENT' ? volunteerMenuItems : organizerMenuItems} onMenuItemClick={handlePersonalMenuClick} />
                <DropdownMenu title="Hoạt động" items={activityMenuItems} onMenuItemClick={handleActivityMenuClick} />
                <DropdownMenu title={user.full_name || user.email} items={userMenuItems} onMenuItemClick={handleUserMenuClick} />
              </>
            ) : (
              <>
                <DropdownMenu title="Cá nhân" items={guestPersonalMenuItems} onMenuItemClick={handlePersonalMenuClick} />
                <DropdownMenu title="Hoạt động" items={activityMenuItems} onMenuItemClick={handleActivityMenuClick} />
                <button
                  onClick={handleLoginButtonClick}
                  className="bg-white text-blue-700 font-bold text-sm py-2 px-6 rounded-lg flex items-center transition-colors duration-200 hover:bg-gray-200"
                >
                  <span className="mr-1.5 text-base">👤</span> Đăng nhập
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
}

export default Header;