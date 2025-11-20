import React from 'react';

function RecentUpdates({ updates = []}) {
  return (
    <div className="w-full mt-8">
      <h2 className="text-xl font-bold text-gray-800 mb-1">Cập nhật gần đây</h2>
      <div className="bg-white p-4 rounded-lg shadow-md">
        <h3 className="text-base font-semibold text-gray-700 mb-3">Thông báo</h3>
        <ul className="list-disc list-inside space-y-1.5 text-gray-600">
          {updates.map((update, index) => (
            <li key={index}>{update}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default RecentUpdates;