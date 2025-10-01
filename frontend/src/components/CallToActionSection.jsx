// import React from 'react';

// function CallToActionSection() {
//   return (
//     <div className="text-center my-12 flex flex-col items-center">
//       <p className="text-lg font-medium text-gray-700 mb-4">SẴN SÀNG TẠO KHÁC BIỆT <span className="text-3xl font-bold mx-2"></span></p>
//       {/* <button className="text-4xl font-extrabold text-gray-900 hover:text-blue-600 transition-colors duration-200">
//         ĐĂNG NHẬP NGAY
//       </button> */}
//        <div className="flex items-center justify-center gap-4">
//         <span className="text-3xl">🔥</span>
//         <button className="border-blue-600 border-2 text-4xl font-extrabold font-mono text-gray-900 hover:text-blue-600 transition-colors duration-200 px-6 py-2 rounded-lg shadow-lg">
//           ĐĂNG NHẬP NGAY
//         </button>
//         {/* <span className="text-3xl">🚀</span> */}
//         <span className="text-3xl">🔥</span>
//        </div>
//     </div>
//   );
// }

// export default CallToActionSection;

import React from 'react';

// Nhận onLoginClick prop
function CallToActionSection({ onLoginClick }) {
  return (
    <div className="text-center my-16 flex flex-col items-center justify-center">
      <p className="text-lg font-medium text-gray-700 mb-4">SẴN SÀNG TẠO KHÁC BIỆT <span className="text-3xl font-bold mx-2"></span></p>
      
      <button
        onClick={() => onLoginClick('login')} // Gọi onLoginClick khi bấm
        className="border-blue-600 border-2 text-4xl font-extrabold font-mono text-gray-900 hover:text-blue-600 transition-colors duration-200 px-6 py-2 rounded-lg shadow-lg"
      >
        ĐĂNG NHẬP NGAY
      </button>
    </div>
  );
}

export default CallToActionSection;