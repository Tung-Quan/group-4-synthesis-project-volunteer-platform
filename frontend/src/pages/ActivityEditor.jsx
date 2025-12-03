import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import apiClient from "../api/apiClient";

function ActivityEditor() {
  	const { activityId } = useParams();
	const navigate = useNavigate();

	const [activity, setActivity] = useState(null);
	const [isLoading, setIsLoading] = useState(true);
	const [error, setError] = useState(null);

	const [title, setTitle] = useState(null);
	const [description, setDescription] = useState(null);
	const [location, setLocation] = useState(null);

	useEffect(() => {
    const fetchActivityDetail = async () => {
      if (!activityId) return;
      try {
        setIsLoading(true);
        setError(null);
        const response = await apiClient.get(`/events/${activityId}`);
        setActivity(response.data);
      } catch (err) {
        setError("Không thể tải thông tin hoạt động này.");
        console.error(`Error fetching activity ${activityId}:`, err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchActivityDetail();
  	}, [activityId]);

	setTitle(activity.title);
	setDescription(activity.description);
	setLocation(activity.location);
	let oldTitle = title;
	let oldDesc = description;
	let oldLoc = location;

	const handleSubmit = async (e) => {
		e.preventDefault();
		setIsLoading(true);
    	setError(null);
	};

	const handleClear = () => {
    	setTitle(oldTitle);
    	setDescription(oldDesc);
		setLocation(oldLoc);
  	};

	if (isLoading) return <div className="text-center p-4">Đang tải...</div>;
	if (error) return <div className="text-center p-4 text-red-500">{error}</div>;

	return (
		<>
			<div className="mb-6">
			<button 
				onClick={() => navigate(-1)}
				className="flex items-center text-gray-700 font-bold font-serif hover:text-blue-600 transition-colors duration-200"
			>
				<svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
				Quay về
			</button>
			</div>

		<form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <label htmlFor="Title" className="block text-gray-700 font-semibold">
            Tên hoạt động
          </label>
          <input
            type="text"
            id="Title"
            className="w-full py-2 px-3 bg-gray-200 border border-gray-400 rounded-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            placeholder={oldTitle}
          />
        </div>

        <div className="space-y-2">
          <label htmlFor="Desc" className="block text-gray-700 font-semibold">
            Chi tiết
          </label>
          <input
            type="text"
            id="Desc"
            className="w-full py-2 px-3 bg-gray-200 border border-gray-400 rounded-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
			placeholder={oldDesc}
          />
        </div>

		<div className="space-y-2">
          <label htmlFor="Location" className="block text-gray-700 font-semibold">
            Địa điểm
          </label>
          <input
            type="text"
            id="Location"
            className="w-full py-2 px-3 bg-gray-200 border border-gray-400 rounded-md shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            required
			placeholder={oldLoc}
          />
        </div>
        
        {error && (
          <div className="text-red-600 text-sm text-center p-2 bg-red-100 rounded">
            {error}
          </div>
        )}

        <div className="flex items-center justify-start space-x-4 pt-2">
          <button
            type="submit"
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-md shadow-md transition-colors duration-200 disabled:bg-blue-300 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Đang xử lý...' : 'Cập nhật'}
          </button>
          <button
            type="button"
            onClick={handleClear}
            className="bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-6 rounded-md shadow-md transition-colors duration-200"
          >
            Hoàn tác
          </button>
        </div>
      	</form>
		</>
	);
}

export default ActivityEditor;