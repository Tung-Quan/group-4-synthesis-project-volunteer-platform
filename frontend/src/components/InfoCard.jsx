import React from 'react';

function InfoCard({ icon, title, description }) {
  return (
    <div className="bg-green-100 p-4 rounded-lg shadow-md flex items-center">
      <span className="text-green-700 text-3xl mr-4">{icon}</span>
      <div>
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
        <p className="text-sm text-gray-600">{description}</p>
      </div>
    </div>
  );
}

export default InfoCard;