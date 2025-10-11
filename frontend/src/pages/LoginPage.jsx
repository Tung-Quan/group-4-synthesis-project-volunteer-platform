import React from 'react';
import Header from '../components/Header';
import PrimaryNavbar from '../components/PrimaryNavBar';
import LoginForm from '../components/LoginForm';
import Footer from '../components/Footer';

function LoginPage({ navigateTo }) {
  return (
    <div className="min-h-screen bg-rose-50 flex flex-col">
      <Header onLoginClick={() => navigateTo('login')} hideLoginButton={true} />
      
      <PrimaryNavbar currentPage="login" navigateTo={navigateTo} />

      <main className="flex-grow max-w-7xl mx-auto p-4 w-full">
        <LoginForm />
      </main>

      <Footer />
    </div>
  );
}

export default LoginPage;