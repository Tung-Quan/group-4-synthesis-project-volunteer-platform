import React from 'react';
import Header from '../components/common/Header';
import LoginForm from '../components/LoginForm';
import Footer from '../components/common/Footer';
// import { useNavigate } from 'react-router-dom';


function LoginPage() {
  // const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-white-200 flex flex-col">
      <Header 
        isLoginPage={true}
      />
      
      <main className="flex-grow max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 w-full flex flex-col items-center justify-center">
        {/* <div className="w-full max-w-4xl mb-4">
          <button 
            onClick={() => navigate('/guest')}
            className="flex items-center text-gray-700 font-serif hover:text-blue-600 transition-colors duration-200"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Quay về trang chủ
          </button>
        </div> */}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch w-full max-w-4xl">
          
          <div className="flex justify-center md:justify-end">
            <LoginForm />
          </div>
          <div className=" justify-start">
            <img 
              src="/loginpicture.jpg"
              alt="University Entrance"
              className="rounded-lg shadow-lg w-full h-full object-cover"
            />
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default LoginPage;