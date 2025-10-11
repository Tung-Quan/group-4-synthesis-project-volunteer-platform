import React from 'react';

function ActivityCard({ title, location, date }) {
  // Hàm để cắt ngắn văn bản nếu quá dài
  const truncateText = (text, maxLength) => {
    if (text.length > maxLength) {
      return text.substring(0, maxLength) + '...';
    }
    return text;
  };

  const truncatedTitle = truncateText(title, 60); 
  const truncatedLocation = truncateText(location, 40); 
  const truncatedDate = truncateText(date, 20); 

  return (
    <div className="mb-2 p-3 bg-gray-700 rounded-md">
      <h4 className="text-white font-medium text-sm leading-tight mb-0.5">{truncatedTitle}</h4>
      <p className="text-gray-300 text-xs">Tại: {truncatedLocation}</p>
      <p className="text-gray-300 text-xs">Ngày: {truncatedDate}</p>
    </div>
  );
}

export default ActivityCard;