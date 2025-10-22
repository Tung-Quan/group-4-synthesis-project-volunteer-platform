// src/data/mockActivities.js

// Dữ liệu chi tiết cho tất cả hoạt động
export const allActivitiesDetails = {
  'MYBK001': {
    id: 'MYBK001',
    title: 'TNV HỖ TRỢ CÔNG TÁC VĂN PHÒNG ĐOÀN KHOA CƠ KHÍ',
    time: '15/09/2025 đến 25/09/2025',
    locationDetail: 'phường Diễn Hồng, TPHCM',
    stats: { maxDays: 2, approvedDays: 0, duration: 1 },
    details: {
      type: 'Hoạt động khác',
      organizerUnit: 'Đoàn trường',
      content: 'Hỗ trợ các công việc văn phòng cho Đoàn khoa Cơ khí trong tuần lễ sinh hoạt công dân.',
      location: 'Văn phòng Đoàn khoa Cơ khí, Cơ sở 1, P. Diễn Hồng',
      organizerName: 'Đỗ Ngọc Lan Phương',
      organizerEmail: 'dongoclanphuongbk@hcmut.edu.vn',
      creationDate: '01/09/2025',
      fileName: 'Mô tả chi tiết.pdf',
      fileUrl: '#',
    }
  },
  'MYBK002': {
    id: 'MYBK002',
    title: 'GIAN HÀNG CHÀO ĐÓN TSV Khóa 2025',
    time: '05/09/2025',
    locationDetail: 'Sân B1, CS1',
    stats: { maxDays: 1, approvedDays: 0, duration: 1 },
    details: {
      type: 'Sự kiện',
      organizerUnit: 'Hội sinh viên',
      content: 'Chào đón tân sinh viên khóa 2025, giới thiệu các câu lạc bộ đội nhóm.',
      location: 'Sân B1, Cơ sở 1',
      organizerName: 'Nguyễn Văn A',
      organizerEmail: 'nguyenvana@hcmut.edu.vn',
      creationDate: '15/08/2025',
      fileName: 'Kế hoạch.pdf',
      fileUrl: '#',
    }
  },
  'MYBK003': {
    id: 'MYBK003',
    title: 'HỘI THẢO CHUYÊN ĐỀ "AI TRONG HỌC TẬP" - BUỔI 1',
    time: '30/10/2025',
    locationDetail: 'Hội trường A5, TPHCM',
    stats: { maxDays: 1, approvedDays: 0, duration: 1 },
    details: {
      type: 'Hội thảo',
      organizerUnit: 'Khoa Khoa học và Kỹ thuật Máy tính',
      content: 'Giới thiệu về các ứng dụng của Trí tuệ Nhân tạo trong học tập và nghiên cứu.',
      location: 'Hội trường A5, Cơ sở 1',
      organizerName: 'TS. Trần Văn B',
      organizerEmail: 'tranvanb@hcmut.edu.vn',
      creationDate: '01/10/2025',
      fileName: 'Nội dung hội thảo.pdf',
      fileUrl: '#',
    }
  },
  'MYBK004': {
    id: 'MYBK004',
    title: 'CUỘC THI BK HACKATHON 2025',
    time: '15/11/2025',
    locationDetail: 'Nhà thi đấu Bách Khoa',
    stats: { maxDays: 2, approvedDays: 0, duration: 2 },
    details: {
      type: 'Cuộc thi',
      organizerUnit: 'CLB Sáng tạo Kỹ thuật',
      content: 'Cuộc thi lập trình nhanh trong 24 giờ dành cho sinh viên.',
      location: 'Nhà thi đấu Bách Khoa, Cơ sở 1',
      organizerName: 'Ban tổ chức BK Hackathon',
      organizerEmail: 'hackathon@hcmut.edu.vn',
      creationDate: '10/10/2025',
      fileName: 'Thể lệ cuộc thi.pdf',
      fileUrl: '#',
    }
  },
  'MYBK005': {
    id: 'MYBK005',
    title: 'NGÀY HỘI HIẾN MÁU NHÂN ĐẠO',
    time: '20/11/2025',
    locationDetail: 'Sảnh H1, Tòa nhà H1',
    stats: { maxDays: 1, approvedDays: 0, duration: 1 },
    details: {
      type: 'Tình nguyện',
      organizerUnit: 'Hội Chữ thập đỏ',
      content: 'Tham gia hiến máu cứu người, một nghĩa cử cao đẹp.',
      location: 'Sảnh H1, Tòa nhà H1, Cơ sở 1',
      organizerName: 'Chị Nguyễn Thị C',
      organizerEmail: 'hienmau@hcmut.edu.vn',
      creationDate: '15/10/2025',
      fileName: 'Thông tin hiến máu.pdf',
      fileUrl: '#',
    }
  },
  'MYBK006': {
    id: 'MYBK006',
    title: 'DỌN DẸP KÝ TÚC XÁ CUỐI HỌC KỲ',
    time: '25/12/2025',
    locationDetail: 'Khu A và Khu B Ký túc xá',
    stats: { maxDays: 1, approvedDays: 0, duration: 1 },
    details: {
      type: 'Tình nguyện',
      organizerUnit: 'Ban quản lý Ký túc xá',
      content: 'Cùng chung tay dọn dẹp, giữ gìn vệ sinh chung cho Ký túc xá.',
      location: 'Khu A và Khu B Ký túc xá Bách Khoa',
      organizerName: 'Anh Lê Văn D',
      organizerEmail: 'ktx@hcmut.edu.vn',
      creationDate: '20/11/2025',
      fileName: 'Kế hoạch dọn dẹp.pdf',
      fileUrl: '#',
    }
  },
};

// --- DANH SÁCH HOẠT ĐỘNG ĐANG DIỄN RA ---
export const currentActivities = [
  { 
    id: 'MYBK001',
    title: 'TNV HỖ TRỢ CÔNG TÁC VĂN PHÒNG ĐOÀN KHOA CƠ KHÍ',
    date: '15/9/2025 đến 25/9/2025',
    location: 'Cơ sở 1, P. Diễn Hồng' 
  },
  { 
    id: 'MYBK002',
    title: 'GIAN HÀNG CHÀO ĐÓN TSV Khóa 2025',
    date: '05/09/2025',
    location: 'Sân B1, CS1' 
  },
  { 
    id: 'MYBK003',
    title: 'HỘI THẢO CHUYÊN ĐỀ "AI TRONG HỌC TẬP" - BUỔI 1',
    date: '30/10/2025',
    location: 'Hội trường A5, TPHCM'
  },
];

// --- DANH SÁCH HOẠT ĐỘNG MỚI ---
export const newActivities = [
  { 
    id: 'MYBK004',
    title: 'CUỘC THI BK HACKATHON 2025',
    date: '15/11/2025',
    location: 'Nhà thi đấu Bách Khoa'
  },
  { 
    id: 'MYBK005',
    title: 'NGÀY HỘI HIẾN MÁU NHÂN ĐẠO',
    date: '20/11/2025',
    location: 'Sảnh H1, Tòa nhà H1'
  },
  { 
    id: 'MYBK006',
    title: 'DỌN DẸP KÝ TÚC XÁ CUỐI HỌC KỲ',
    date: '25/12/2025',
    location: 'Khu A và Khu B Ký túc xá'
  },
];
export const managedActivities = [
  { 
    id: 'MYBK001',
    title: 'TNV HỖ TRỢ CÔNG TÁC VĂN PHÒNG ĐOÀN KHOA CƠ KHÍ',
    date: '15/9/2025 đến 25/9/2025',
    location: 'Cơ sở 1, P. Diễn Hồng' 
  },
  { 
    id: 'MYBK002',
    title: 'GIAN HÀNG CHÀO ĐÓN TSV Khóa 2025',
    date: '05/09/2025',
    location: 'Sân B1, CS1' 
  },
  { 
    id: 'MYBK004',
    title: 'CUỘC THI BK HACKATHON 2025',
    date: '15/11/2025',
    location: 'Nhà thi đấu Bách Khoa'
  },
];

export const allActivitiesForSearch = Object.values(allActivitiesDetails).map(activity => ({
  id: activity.id,
  title: activity.title,
  date: activity.time,
  location: activity.locationDetail,
}));

export const getTitle = (id) => {
  const activity = allActivitiesForSearch.find((activity) => activity.id === id);

  if (activity) {
    return activity.title;
  }

  return '';
}

// --- DỮ LIỆU CHO CÁC CẬP NHẬT GẦN ĐÂY ---
export const recentUpdates = [
    'Hoạt động "TNV HỖ TRỢ CÔNG TÁC VĂN PHÒNG..." đã được cập nhật.',
    'Hoạt động "GIAN HÀNG CHÀO ĐÓN TSV Khóa 2025" đã hết hạn đăng ký.',
    'Hoạt động mới "CUỘC THI BK HACKATHON 2025" vừa được thêm.',
];