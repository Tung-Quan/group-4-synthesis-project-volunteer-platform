import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SearchSection() {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const handleSearch = (e) => {
    e.preventDefault(); 
    if (searchTerm.trim()) { 
      navigate(`/search?q=${encodeURIComponent(searchTerm)}`);    
    }
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-center bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-3xl font-extrabold font-serif text-gray-800 mb-6 uppercase">
        Tìm kiếm hoạt động
      </h2>
      <form onSubmit={handleSearch} className="relative w-full max-w-md">
        <input
          type="text"
          placeholder="Nhập tên hoạt động, địa điểm,..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full py-3 pl-4 pr-12 border-2 border-gray-300 rounded-full focus:outline-none focus:border-blue-500"
        />
        <button 
          type="submit"
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-blue-600"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        </button>
      </form>
    </div>
  );
}
export default SearchSection;