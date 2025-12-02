import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/apiClient';

// Component con để quản lý một slot trong form
const SlotInput = ({ index, slot, updateSlot, removeSlot }) => {
  const handleChange = (e) => {
    updateSlot(index, { ...slot, [e.target.name]: e.target.value });
  };

  return (
    <div className="p-4 border border-gray-200 rounded-lg relative space-y-3">
      <button 
        type="button" 
        onClick={() => removeSlot(index)}
        className="absolute top-2 right-2 text-red-500 hover:text-red-700 font-bold"
      >
        &times;
      </button>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Ngày làm việc</label>
          <input type="date" name="work_date" value={slot.work_date} onChange={handleChange} required className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"/>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Ngày CTXH thưởng</label>
          <input type="number" name="day_reward" value={slot.day_reward} onChange={handleChange} required step="0.1" min="0" className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"/>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Giờ bắt đầu</label>
          <input type="time" name="starts_at" value={slot.starts_at} onChange={handleChange} required className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"/>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Giờ kết thúc</label>
          <input type="time" name="ends_at" value={slot.ends_at} onChange={handleChange} required className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"/>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Số lượng</label>
          <input type="number" name="capacity" value={slot.capacity} onChange={handleChange} required min="1" className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"/>
        </div>
      </div>
    </div>
  );
};

function CreateNewActivityPage() {
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  
  // State cho thông tin chung của sự kiện
  const [eventData, setEventData] = useState({
    title: '',
    description: '',
    location: '',
  });

  // State cho mảng các slots
  const [slots, setSlots] = useState([
    { work_date: '', starts_at: '', ends_at: '', capacity: 10, day_reward: 1.0 }
  ]);

  const handleEventChange = (e) => {
    setEventData({ ...eventData, [e.target.name]: e.target.value });
  };

  const addSlot = () => {
    setSlots([...slots, { work_date: '', starts_at: '', ends_at: '', capacity: 10, day_reward: 1.0 }]);
  };

  const removeSlot = (index) => {
    if (slots.length <= 1) {
      alert("Phải có ít nhất một ca làm việc.");
      return;
    }
    const newSlots = slots.filter((_, i) => i !== index);
    setSlots(newSlots);
  };

  const updateSlot = (index, updatedSlot) => {
    const newSlots = slots.map((slot, i) => i === index ? updatedSlot : slot);
    setSlots(newSlots);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    const payload = {
      ...eventData,
      slots: slots,
    };

    try {
      // Gọi API POST /events/ theo tài liệu
      const response = await apiClient.post('/events/', payload);
      alert("Tạo hoạt động mới thành công!");
      navigate('/organizer/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || "Đã có lỗi xảy ra khi tạo hoạt động.");
      console.error("Failed to create event:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <div className="mb-4">
          <button 
            onClick={() => navigate(-1)}
            className="flex items-center text-gray-700 font-bold font-serif hover:text-blue-600 transition-colors duration-200"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Quay về
          </button>
        </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Phần thông tin chung */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Thông tin chung</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Tên hoạt động</label>
              <input type="text" name="title" value={eventData.title} onChange={handleEventChange} required className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Mô tả</label>
              <textarea name="description" value={eventData.description} onChange={handleEventChange} required rows="4" className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"></textarea>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Địa điểm chung</label>
              <input type="text" name="location" value={eventData.location} onChange={handleEventChange} required className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"/>
            </div>
          </div>
        </div>

        {/* Phần quản lý Slots */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">Các ca làm việc (Slots)</h2>
            <button type="button" onClick={addSlot} className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-lg">
              Thêm ca
            </button>
          </div>
          <div className="space-y-4">
            {slots.map((slot, index) => (
              <SlotInput 
                key={index}
                index={index}
                slot={slot}
                updateSlot={updateSlot}
                removeSlot={removeSlot}
              />
            ))}
          </div>
        </div>
        
        {error && <div className="text-red-500 text-center p-2 bg-red-100 rounded">{error}</div>}

        {/* Nút Submit */}
        <div className="flex justify-end">
          <button 
            type="submit" 
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg text-lg disabled:bg-blue-300"
          >
            {isLoading ? 'Đang tạo...' : 'Tạo hoạt động'}
          </button>
        </div>
      </form>
    </>
  );
}

export default CreateNewActivityPage;