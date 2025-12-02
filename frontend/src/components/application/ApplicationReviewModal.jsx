import React from 'react';
import { useState, useEffect } from 'react';

function ApplicationReviewModal({ isOpen, onClose, approved, slotId, stuNo, onSave }) {
	const [note, setNote] = useState('');
	useEffect(() => {setNote('')}, [setNote]);

	if (!isOpen) return null;

	const handleSave = () => {
		onSave({
			slot_id: slotId,
			student_user_id: stuNo,
			note: note,
			status: approved //this is a bool
		});
	};

	return (
		<div
			className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
			onClick={onClose}
		>
			<div
				className="bg-white rounded-lg shadow-xl w-full max-w-md flex flex-col"
				onClick={e => e.stopPropagation()}
			>
				<div className="flex justify-between items-center p-4 border-b border-gray-300">
					<h2 className="text-xl font-bold text-gray-800">Nhập lí do</h2>
					<button onClick={onClose} className="text-gray-500 hover:text-gray-800 text-2xl font-bold">&times;</button>
				</div>
				<div className="p-6 space-y-4">
					<div>
						<label htmlFor="Note" className="block text-sm font-medium text-gray-700">
						</label>
						<input
							type="text"
							id="Note"
							value={note}
							onChange={(e) => setNote(e.target.value)}
							className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
						/>
					</div>
				</div>
				<div className="flex justify-end items-center p-4 border-t border-gray-300 space-x-3">
					<button
						onClick={onClose}
						className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg"
					>
						Hủy
					</button>
					<button
						onClick={handleSave}
						className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg"
					>
						Gửi
					</button>
				</div>
			</div>
		</div>
	);
}

export default ApplicationReviewModal;