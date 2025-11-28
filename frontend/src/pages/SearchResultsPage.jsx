// import React, { useEffect, useState } from 'react';
// import Header from '../components/common/Header';
// import Footer from '../components/common/Footer';
// import ActivityListItem from '../components/activity/ActivityListItem';
// import { allActivitiesForSearch } from '../mockdata/mockActivities.js';
// import SearchSection from '../components/home/SearchSection';
// import { useNavigate, useSearchParams } from 'react-router-dom';


// function SearchResultsPage() {
//   const [results, setResults] = useState([]);
//   const navigate = useNavigate();
//   const [searchParams] = useSearchParams();
//   const searchQuery = searchParams.get('query') || '';

//   // Giả lập logic tìm kiếm
//   useEffect(() => {
//     if (searchQuery) {
//       const lowercasedQuery = searchQuery.toLowerCase();
//       const filteredResults = allActivitiesForSearch.filter(activity => 
//         activity.title.toLowerCase().includes(lowercasedQuery) ||
//         activity.location.toLowerCase().includes(lowercasedQuery)
//       );
//       setResults(filteredResults);
//     }
//   }, [searchQuery]);

//   return (
//     <>
//         <div className="mb-2">
//           <SearchSection />
//         </div>

//         {/* Nút Back */}
//         <div className="mb-4">
//           <button 
//             onClick={() => navigate(-1)}
//             className="flex items-center text-gray-700 font-bold font-serif hover:text-blue-600 transition-colors duration-200"
//           >
//             <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
//             Quay về
//           </button>
//         </div>
        
//         <h1 className="text-3xl font-serif font-bold text-center text-gray-800 my-6">
//           Kết quả tìm kiếm cho: "<span className="text-blue-600">{searchQuery}</span>"
//         </h1>

//         <div className="bg-white p-6 rounded-lg shadow-md">
//           {results.length > 0 ? (
//             results.map(activity => (
//               <ActivityListItem 
//                 key={activity.id} 
//                 activity={activity}
//               />
//             ))
//           ) : (
//             <p className="text-center text-gray-500">Không tìm thấy hoạt động nào phù hợp.</p>
//           )}
//         </div>
//     </>
//   );
// }

// export default SearchResultsPage;

import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import apiClient from '../api/apiClient';
import ActivityListItem from '../components/activity/ActivityListItem';
import SearchSection from '../components/home/SearchSection';

function SearchResultsPage() {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const searchQuery = searchParams.get('q') || ''; // API dùng 'q' thay vì 'query'

  useEffect(() => {
    if (!searchQuery.trim()) {
      setResults([]);
      return;
    }

    const performSearch = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await apiClient.get(`/events/search?q=${encodeURIComponent(searchQuery)}`);
        setResults(response.data);
      } catch (err) {
        if (err.response?.status === 404) {
          setResults([]); // Không tìm thấy kết quả
        } else {
          setError("Có lỗi xảy ra khi tìm kiếm.");
        }
        console.error("Search failed:", err);
      } finally {
        setIsLoading(false);
      }
    };

    performSearch();
  }, [searchQuery]);

  return (
    <>
      <div className="mb-2">
        <SearchSection />
      </div>

      <div className="mb-4">
        <button onClick={() => navigate(-1)} className="...">Quay về</button>
      </div>

      <h1 className="text-3xl font-serif font-bold text-center text-gray-800 my-6">
        Kết quả tìm kiếm cho: "<span className="text-blue-600">{searchQuery}</span>"
      </h1>

      <div className="bg-white p-6 rounded-lg shadow-md">
        {isLoading ? (
          <p className="text-center text-gray-500">Đang tìm kiếm...</p>
        ) : error ? (
          <p className="text-center text-red-500">{error}</p>
        ) : results.length > 0 ? (
          results.map(event => (
            <ActivityListItem
              key={event.event_id}
              activity={{
                id: event.event_id,
                title: event.event_name,
                location: event.location || 'N/A',
                // API search trả về 1 mảng slots, ta có thể lấy ngày của slot đầu tiên
                date: event.slots?.length > 0
                  ? new Date(event.slots[0].work_date).toLocaleDateString('vi-VN')
                  : 'N/A',
              }}
            />
          ))
        ) : (
          <p className="text-center text-gray-500">Không tìm thấy hoạt động nào phù hợp.</p>
        )}
      </div>
    </>
  );
}

export default SearchResultsPage;