import React, { useState } from 'react';

function DropdownMenu({ title, items, onMenuItemClick = () => {} }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div 
      className="relative" 
      onMouseEnter={() => setIsOpen(true)} 
      onMouseLeave={() => setIsOpen(false)}
    >
      <button
        className="flex items-center text-white font-semibold py-1 px-3 rounded-md bg-blue-700 border border-white/50 hover:bg-blue-600 transition-colors duration-200"
      >
        <svg className="w-4 h-4 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"/></svg>
        <span className="ml-1">{title}</span>
      </button>

      {isOpen && (
        <div className="absolute right-0 w-56 bg-gray-700 rounded-md shadow-lg z-20 border border-black/50">
          <div className="py-1">
            {items.map((item, index) => (
              <a
                key={index}
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  onMenuItemClick(item);
                  setIsOpen(false); // Đóng menu sau khi cclick
                }}
                className={`block px-4 py-2 text-base text-gray-200 hover:bg-gray-600 ${index < items.length - 1 ? 'border-b border-gray-500' : ''}`}
              >
                {item}
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default DropdownMenu;