import React from 'react';

function ActivityCard({ title, location, date }) {
  // Hàm để cắt ngắn văn bản nếu quá dài
  const truncateText = (text, maxLength) => {
    if (text.length > maxLength) {
      return text.substring(0, maxLength) + '...';
    }
    return text;
  };

  const truncatedTitle = truncateText(title, 60); // Cắt ngắn tiêu đề
  const truncatedLocation = truncateText(location, 40); // Cắt ngắn địa điểm
  const truncatedDate = truncateText(date, 20); // Cắt ngắn ngày

  return (
    // Giảm padding, giảm mb, bg-gray-600 => bg-gray-700 để khớp hơn với hình ảnh
    <div className="mb-2 p-3 bg-gray-700 rounded-md">
      {/* text-sm cho tiêu đề, leading-tight để giảm khoảng cách dòng */}
      <h4 className="text-white font-medium text-sm leading-tight mb-0.5">{truncatedTitle}</h4>
      {/* text-xs cho thông tin chi tiết */}
      <p className="text-gray-300 text-xs">Tại: {truncatedLocation}</p>
      <p className="text-gray-300 text-xs">Ngày: {truncatedDate}</p>
    </div>
  );
}

export default ActivityCard;