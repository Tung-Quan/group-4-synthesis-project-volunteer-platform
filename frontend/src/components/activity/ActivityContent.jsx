import React from 'react';

const ContentRow = ({ label, children }) => (
  <div className="grid grid-cols-[max-content,1fr] gap-x-2 py-1 item-start">
    <span className="font-semibold text-gray-800 text-right">{label}:</span>
    <span className="text-gray-700 break-all">{children}</span>
  </div>
);


function ActivityContent({ details }) {
  return (
    <div className="space-y-1 text-base">
      <ContentRow label="Loại hoạt động">{details.type}</ContentRow>
      <ContentRow label="Đơn vị tổ chức">{details.organizerUnit}</ContentRow>
      <ContentRow label="Nội dung">{details.content}</ContentRow>
      <ContentRow label="Địa điểm">{details.location}</ContentRow>
      <ContentRow label="Người tổ chức">{details.organizerName}</ContentRow>
      <ContentRow label="Email người tổ chức">
        <a href={`mailto:${details.organizerEmail}`} className="text-blue-600 hover:underline">
          {details.organizerEmail}
        </a>
      </ContentRow>
      <ContentRow label="Điện thoại người tổ chức">{details.organizerPhone || 'N/A'}</ContentRow>
      <ContentRow label="Ngày tạo hoạt động">{details.creationDate}</ContentRow>
      <ContentRow label="Văn bản thông báo">
        <a href={details.fileUrl} className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
          {details.fileName}
        </a>
      </ContentRow>
      <ContentRow label="File minh chứng của HĐ">{details.proofFile || '--'}</ContentRow>
    </div>
  );
}

export default ActivityContent;