import axios from 'axios';

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
    withCredentials: true,
    timeout: 10000, //timeout 10 giây
});

// dùng để lưu trữ CSRF token
let csrfToken = null;

export const setCsrfToken = (token) => {
    console.log("CSRF Token set in apiClient:", token);
    csrfToken = token;
};

// Interceptor này sẽ chạy TRƯỚC KHI một request được gửi đi.
apiClient.interceptors.request.use(
    (config) => {
        const methodsWithCsrf = ['post', 'put', 'patch', 'delete'];
        if (methodsWithCsrf.includes(config.method.toLowerCase())) {
            if (csrfToken) {
                config.headers['X-CSRF-Token'] = csrfToken;
                console.log("Attached CSRF Token to request header:", csrfToken);
            } else {
                console.warn("CSRF Token is not available for this request.");
            }
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Interceptor này sẽ chạy SAU KHI nhận được response từ backend.
let isRefreshing = false;
let failedQueue = [];
const processQueue = (error, token = null) => {
    failedQueue.forEach(prom => {
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token);
        }
    });
    failedQueue = [];
};

apiClient.interceptors.response.use(
    (response) => {
        // Nếu response thành công, không làm gì cả, chỉ trả về response
        return response;
    },
    async (error) => {
        const originalRequest = error.config;

        // Chỉ xử lý lỗi 401 và đây không phải là request thử lại
        if (error.response?.status === 401 && !originalRequest._retry) {
            if (isRefreshing) {
                return new Promise((resolve, reject) => {
                    failedQueue.push({ resolve, reject });
                })
                    .then(token => {
                        originalRequest.headers['Authorization'] = 'Bearer ' + token; 
                        return apiClient(originalRequest);
                    })
                    .catch(err => {
                        return Promise.reject(err);
                    });
            }

            originalRequest._retry = true;
            isRefreshing = true;

            try {
                const refreshResponse = await apiClient.post('/auth/refresh');
                console.log("Token refreshed successfully.");
                processQueue(null, null);

                return apiClient(originalRequest);

            } catch (refreshError) {
                console.error("Failed to refresh token:", refreshError);
                processQueue(refreshError, null);
                // có thể gọi hàm logout từ AuthContext ở đây)
                window.location.href = '/login';
                return Promise.reject(refreshError);
            } finally {
                isRefreshing = false;
            }
        }
        return Promise.reject(error);
    }
);

export default apiClient;