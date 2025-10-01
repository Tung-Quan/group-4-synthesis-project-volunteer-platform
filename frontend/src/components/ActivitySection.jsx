import React from 'react';
import ActivityCard from './ActivityCard';

function ActivitySection({ title, activities }) {
  return (
    <div className="bg-gray-800 p-5 rounded-lg shadow-xl">
      <h2 className="text-green-400 font-semibold text-xl mb-4">{title} &gt;&gt;&gt;</h2>
      {/* Thêm max-h-64 (hoặc bất kỳ chiều cao nào bạn muốn) và overflow-y-auto */}
      <div className="space-y-3 max-h-64 overflow-y-auto pr-2"> {/* pr-2 để scrollbar không dính vào text */}
        {activities.map((activity, index) => (
          <ActivityCard
            key={index}
            title={activity.title}
            location={activity.location}
            date={activity.date}
          />
        ))}
      </div>
    </div>
  );
}

export default ActivitySection;