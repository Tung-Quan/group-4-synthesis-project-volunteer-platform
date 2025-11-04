import React from 'react';

const StatCard = ({ label, value, colorClass }) => (
  <div className="text-center">
    <p className={`text-sm font-semibold ${colorClass}`}>{label}</p>
    <p className={`text-4xl font-bold ${colorClass}`}>{value}</p>  
  </div>
);

function ActivityStats({ maxDays, approvedDays, duration }) {
  return (
    <div className="flex justify-around items-center py-4">
      <StatCard label="NGÀY CTXH TỐI ĐA" value={maxDays} colorClass="text-red-600" />
      <StatCard label="NGÀY CTXH ĐÃ DUYỆT" value={approvedDays} colorClass="text-green-600" />
      <StatCard label="THỜI LƯỢNG THỰC HIỆN" value={duration} colorClass="text-gray-700" />
    </div>
  );
}

export default ActivityStats;