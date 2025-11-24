import React from 'react';

// Component con cho từng ca trong danh sách
const ShiftListItem = ({ shift, onRegister }) => {
    const isFull = shift.registered >= shift.capacity;
    return (
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-3 border-b border-gray-200 last:border-b-0">
            <div>
                <p className="font-semibold text-gray-800">Thời gian: {shift.time}</p>
                <p className="text-sm text-gray-600">Địa điểm: {shift.location}</p>
                <p className="text-sm text-blue-600">Số lượng: {shift.registered} / {shift.capacity}</p>
            </div>
            <button
                onClick={() => onRegister(shift.id)}
                disabled={isFull}
                className={`mt-2 sm:mt-0 font-bold py-2 px-5 rounded-lg text-sm transition-colors duration-200
          ${isFull
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : 'bg-green-600 hover:bg-green-700 text-white'
                    }`}
            >
                {isFull ? 'Đã đầy' : 'Đăng ký'}
            </button>
        </div>
    );
};


function ShiftsModal({ isOpen, onClose, shifts = [], onRegisterShift, activityTitle }) {
    if (!isOpen) return null;

    return (
        // Lớp phủ nền
        <div
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
            onClick={onClose} // Bấm ra ngoài để đóng
        >
            {/* Khung nội dung modal */}
            <div
                className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] flex flex-col"
                onClick={e => e.stopPropagation()} // Ngăn việc bấm vào modal làm nó bị đóng
            >
                {/* Header của Modal */}
                <div className="flex justify-between items-center p-4 border-b border-gray-300">
                    <div>
                        <h2 className="text-xl font-bold text-gray-800">Chọn ca làm việc</h2>
                        <p className="text-sm text-gray-600">{activityTitle}</p>
                    </div>
                    <button onClick={onClose} className="text-gray-500 hover:text-gray-800 text-2xl font-bold">&times;</button>
                </div>

                {/* Danh sách các ca (có thể cuộn) */}
                <div className="overflow-y-auto">
                    {shifts.length > 0 ? (
                        shifts.map(shift => (
                            <ShiftListItem key={shift.id} shift={shift} onRegister={onRegisterShift} />
                        ))
                    ) : (
                        <p className="p-6 text-center text-gray-500">Không có ca làm việc nào cho hoạt động này.</p>
                    )}
                </div>
            </div>
        </div>
    );
}

export default ShiftsModal;