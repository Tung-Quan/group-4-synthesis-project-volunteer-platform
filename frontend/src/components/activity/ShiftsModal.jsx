import React, { useState } from 'react';

// Component con cho từng ca
const ShiftListItem = ({ shift, onSelect, isSelected }) => {
    const isFull = shift.registered >= shift.capacity;
    return (
        <div
            className={`p-3 border-b border-gray-200 last:border-b-0 transition-colors duration-200 ${isSelected ? 'bg-blue-50' : ''}`}
        >
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between">
                <div>
                    <p className="font-semibold text-gray-800">Thời gian: {shift.time}</p>
                    <p className="text-sm text-gray-600">Địa điểm: {shift.location}</p>
                    <p className="text-sm text-blue-600">Số lượng: {shift.registered} / {shift.capacity}</p>
                </div>
                <button
                    onClick={() => onSelect(shift.id)}
                    disabled={isFull}
                    className={`mt-2 sm:mt-0 font-bold py-2 px-5 rounded-lg text-sm transition-colors duration-200
            ${isFull
                            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                            : isSelected
                                ? 'bg-yellow-500 hover:bg-yellow-600 text-white'
                                : 'bg-green-600 hover:bg-green-700 text-white'
                        }`}
                >
                    {isFull ? 'Đã đầy' : isSelected ? 'Đang chọn' : 'Chọn ca này'}
                </button>
            </div>
        </div>
    );
};


function ShiftsModal({ isOpen, onClose, shifts = [], onRegisterShift, activityTitle }) {
    // State để theo dõi ca nào đang được chọn
    const [selectedShiftId, setSelectedShiftId] = useState(null);
    // State để lưu nội dung ghi chú
    const [note, setNote] = useState('');

    if (!isOpen) return null;

    const handleSelectShift = (shiftId) => {
        // Nếu bấm lại ca đang chọn, bỏ chọn nó. Ngược lại, chọn ca mới.
        setSelectedShiftId(prevId => (prevId === shiftId ? null : shiftId));
    };

    const handleConfirmRegistration = () => {
        if (!selectedShiftId) {
            alert("Vui lòng chọn một ca làm việc.");
            return;
        }
        // Gọi hàm onRegisterShift từ cha với cả shiftId và note
        onRegisterShift(selectedShiftId, note);
    };

    const handleClose = () => {
        // Reset state khi đóng modal
        setSelectedShiftId(null);
        setNote('');
        onClose();
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={handleClose}>
            <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] flex flex-col" onClick={e => e.stopPropagation()}>
                <div className="flex justify-between items-center p-4 border-b border-gray-300">
                    <div>
                        <h2 className="text-xl font-bold text-gray-800">Chọn ca làm việc</h2>
                        <p className="text-sm text-gray-600">{activityTitle}</p>
                    </div>
                    <button onClick={handleClose} className="text-gray-500 hover:text-gray-800 text-2xl font-bold">&times;</button>
                </div>

                {/* Danh sách các ca */}
                <div className="overflow-y-auto">
                    {shifts.length > 0 ? (
                        shifts.map(shift => (
                            <ShiftListItem
                                key={shift.id}
                                shift={shift}
                                onSelect={handleSelectShift}
                                isSelected={selectedShiftId === shift.id}
                            />
                        ))
                    ) : (
                        <p className="p-6 text-center text-gray-500">Không có ca làm việc nào cho hoạt động này.</p>
                    )}
                </div>

                {/* === PHẦN NHẬP GHI CHÚ VÀ XÁC NHẬN === */}
                {/* Chỉ hiển thị khi đã có một ca được chọn */}
                {selectedShiftId && (
                    <div className="p-4 border-t border-gray-200 bg-gray-50">
                        <label htmlFor="note" className="block text-sm font-medium text-gray-700 mb-2">
                            Ghi chú cho nhà tổ chức (tùy chọn)
                        </label>
                        <textarea
                            id="note"
                            rows={3}
                            value={note}
                            onChange={(e) => setNote(e.target.value)}
                            placeholder="Ví dụ: Em có kinh nghiệm về sơ cứu, em có thể đến trễ 15 phút,..."
                            className="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        ></textarea>
                    </div>
                )}

                {/* Footer của Modal */}
                <div className="flex justify-end items-center p-4 border-t border-gray-300 space-x-3">
                    <button onClick={handleClose} className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg">
                        Hủy
                    </button>
                    <button
                        onClick={handleConfirmRegistration}
                        // Nút này chỉ bật khi đã chọn một ca
                        disabled={!selectedShiftId}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg disabled:bg-blue-300 disabled:cursor-not-allowed"
                    >
                        Xác nhận Đăng ký
                    </button>
                </div>
            </div>
        </div>
    );
}

export default ShiftsModal;