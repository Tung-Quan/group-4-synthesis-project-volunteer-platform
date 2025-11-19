import React from 'react';

function AboutAndCTASection({ navigateTo }) {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex flex-col md:flex-row items-center justify-between gap-12">
      
      {/*About Us */}
      <div className="w-full md:w-3/5">
        <p className="font-serif text-base md:text-lg text-gray-700 leading-relaxed">
          Xin chào các chiến binh Bách Khoa! Bạn đang tìm kiếm những hoạt động công tác xã hội "chất lừ"? Bạn muốn đóng góp sức trẻ cho cộng đồng nhưng chưa biết bắt đầu từ đâu? Bach Khoa Volunteer Hub chính là nơi dành cho bạn!
        </p>
        <p className="font-serif text-base md:text-lg text-gray-700 leading-relaxed mt-4">
          Tại đây, bạn có thể dễ dàng tìm kiếm, đăng ký tham gia các hoạt động phù hợp, đồng thời tích lũy ngày công tác xã hội và điểm rèn luyện một cách minh bạch. Đối với các đơn vị tổ chức, nền tảng cung cấp công cụ quản lý chiến dịch hiệu quả, từ việc đăng tải hoạt động, duyệt đơn, đến điểm danh và báo cáo.
        </p>
        <p className="font-serif text-base md:text-lg text-gray-700 leading-relaxed mt-4">
          Cùng nhau, chúng ta xây dựng một cộng đồng Bách Khoa năng động, sáng tạo.
        </p>
      </div>

      {/* Call to Action */}
      <div className="w-full md:w-auto flex justify-center md:justify-end">
        <div className="border-2 border-dashed border-gray-400 rounded-lg p-6 text-center">
          <p className="text-base font-medium text-gray-700 mb-2">SẴN SÀNG TẠO KHÁC BIỆT CHƯA</p>
          <button
            onClick={() => navigateTo('/login')}
            className="text-2xl font-extrabold text-blue-700 hover:text-blue-500 transition-colors duration-200 cursor-pointer"
          >
            ĐĂNG NHẬP NGAY
          </button>
        </div>
      </div>

    </div>
  );
}

export default AboutAndCTASection;