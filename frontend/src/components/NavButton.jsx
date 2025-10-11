import React  from "react";

function NavButton(icon, title)
{
	return (
    <div className="bg-green-100 p-4 rounded-lg shadow-md flex items-center">
      <span className="text-green-700 text-3xl mr-4">{icon}</span>
      <div>
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
      </div>
    </div>
  );
}

export default NavButton;