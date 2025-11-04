import React, { useState } from 'react';
import DropdownMenu from './DropdownMenu.jsx';

function Header({ isLoginPage = false, isLoggedIn, onLogout, user, navigateTo }) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const volunteerMenuItems = ['Hoạt động đang tham gia', 'Lịch sử tham gia'];
  const activityMenuItems = ['Hoạt động đang diễn ra', 'Hoạt động mới'];
  const userMenuItems = ['Hồ sơ', 'Đăng xuất'];
  const organizerMenuItems = ['Duyệt đơn đăng kí', 'Quản lý hoạt động'];
  // const personalMenuItems = ['Hoạt động đang tham gia', 'Lịch sử tham gia'];
  const guestPersonalMenuItems = [...volunteerMenuItems, ...organizerMenuItems];

  const handleUserMenuClick = (item) => {
    if (item === 'Đăng xuất') {
      onLogout();
    }
    setIsMobileMenuOpen(false); 
  };
  
  const handlePersonalMenuClick = (item) => {
    let targetPage = null;
    // Volunteer actions
    if (item === 'Hoạt động đang tham gia') targetPage = 'participating-activities';
    if (item === 'Lịch sử tham gia') targetPage = 'history-activities';
    
    // Organizer actions
    if (item === 'Duyệt đơn đăng kí') targetPage = 'application-review';
    if (item === 'Quản lý hoạt động') targetPage = 'activity-dashboard';

    if (!isLoggedIn && targetPage) {
      navigateTo('login', { redirectAfterLogin: targetPage });
    } else if (targetPage) {
      navigateTo(targetPage);
    }
    setIsMobileMenuOpen(false);
  }    
  const handleLoginButtonClick = () => {
    navigateTo('login');
    setIsMobileMenuOpen(false);
  };
  
  const handleActivityMenuClick = (item) => {
    let targetPage = null;
    switch (item) {
      //Activity info
      //Allow both volunteers and organizers to see
      case 'Hoạt động mới':
        targetPage = 'new-activities'; //implemented
        break;

      case 'Hoạt động đang diễn ra':
        targetPage = 'current-activities'; //implemented
        break;

      default:
        break;
    }

    if(!isLoggedIn && targetPage){
      navigateTo('login', { redirectAfterLogin: targetPage });
      return;
    }

    if (targetPage) {
      navigateTo(targetPage);
    }
    setIsMobileMenuOpen(false);
  };

  return (
    <header className="bg-blue-700 px-4 sm:px-6 py-3 flex items-center justify-between shadow-lg h-16 relative">
      <div className="flex items-center">
        <img src="/icon.svg" alt="Bach Khoa Logo" className="h-10 w-auto mr-3" />
        <h1 className="text-xl md:text-2xl font-extrabold text-white" style={{ textShadow: '0 0 2px black, 0 0 2px black, 0 0 2px black, 0 0 2px black' }}>
          Bach Khoa Volunteer Hub
        </h1>
      </div>

      <div className="hidden md:flex items-center space-x-4">
        {isLoggedIn && user ? (
          <>
            <DropdownMenu title={user.type === 'VOLUNTEER' ? 'Cá nhân' : 'Quản lý'} items={user.type === 'VOLUNTEER' ? volunteerMenuItems : organizerMenuItems} onMenuItemClick={handlePersonalMenuClick} />
            <DropdownMenu title="Hoạt động" items={activityMenuItems} onMenuItemClick={handleActivityMenuClick} />
            <DropdownMenu title={user.display_name} items={userMenuItems} onMenuItemClick={handleUserMenuClick} />
          </>
        ) : (
          !isLoginPage && (
            <>
              <DropdownMenu title="Cá nhân" items={guestPersonalMenuItems} onMenuItemClick={handlePersonalMenuClick}/>
              <DropdownMenu 
                title="Hoạt động" 
                items={activityMenuItems} 
                onMenuItemClick={handleActivityMenuClick} 
              />
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

      {/* Nút Hamburger - Dành cho màn hình Mobile */}      
      {!isLoginPage && (
        <div className="md:hidden">
          <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="text-white focus:outline-none">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-8 6h8"></path>
            </svg>
          </button>
        </div>
      )}

      {/* Menu xổ xuống trên Mobile - Kích hoạt bằng nút Hamburger */}
      {isMobileMenuOpen && !isLoginPage && (
        <div className="md:hidden absolute top-16 left-0 w-full bg-blue-800 shadow-lg z-20">
          <div className="flex flex-col items-center space-y-4 py-4">
            {isLoggedIn && user ? (
              
              <>
                <DropdownMenu title={user.type === 'VOLUNTEER' ? 'Cá nhân' : 'Quản lý'} items={user.type === 'VOLUNTEER' ? volunteerMenuItems : organizerMenuItems} onMenuItemClick={handlePersonalMenuClick}/>
                <DropdownMenu 
                  title="Hoạt động" 
                  items={activityMenuItems} 
                  onMenuItemClick={handleActivityMenuClick} 
                />
                <DropdownMenu 
                  title={user.display_name} 
                  items={userMenuItems} 
                  onMenuItemClick={handleUserMenuClick} 
                />
              </>
            ) : (
              
              <>
                <DropdownMenu title="Cá nhân" items={guestPersonalMenuItems} onMenuItemClick={handlePersonalMenuClick}/>
                <DropdownMenu 
                  title="Hoạt động" 
                  items={activityMenuItems} 
                  onMenuItemClick={handleActivityMenuClick} 
                />
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