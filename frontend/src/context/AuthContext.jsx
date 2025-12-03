import React, { createContext, useState, useContext, useEffect } from 'react';
import apiClient, { setCsrfToken } from '../api/apiClient'; // Import setCsrfToken

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
    //     const checkUserStatus = async () => {
    //         try {
    //             const userResponse = await apiClient.get('/users/profile/me');
    //             const userData = userResponse.data;
    //             setUser(userData);
    //             setIsLoggedIn(true);

    //             // ==========================================================
    //             // === BƯỚC 2: NẾU ĐÃ ĐĂNG NHẬP, LẤY LẠI CSRF TOKEN MỚI ===
    //             // ==========================================================
    //             try {
    //                 const csrfResponse = await apiClient.get('/auth/csrf');
    //                 const newCsrfToken = csrfResponse.data.csrf_token;
    //                 // Nạp token mới vào apiClient để sử dụng cho các request sau
    //                 setCsrfToken(newCsrfToken);
    //             } catch (csrfError) {
    //                 console.error("Failed to fetch CSRF token on reload:", csrfError);
    //                 // Nếu không lấy được CSRF, coi như logout để đảm bảo an toàn
    //                 setUser(null);
    //                 setIsLoggedIn(false);
    //             }

    //         } catch (error) {
    //             console.log("User is not logged in on reload.");
    //             setUser(null);
    //             setIsLoggedIn(false);
    //         } finally {
    //             setIsLoading(false);
    //         }
    //     };

    //     checkUserStatus();
    // }, []);
        const initializeAuth = async () => {
            try {
                const userResponse = await apiClient.get('/users/profile/me');
                const userData = userResponse.data;
                
                setUser(userData);
                setIsLoggedIn(true);

                try {
                    const csrfResponse = await apiClient.get('/auth/csrf');
                    const newCsrfToken = csrfResponse.data.csrf_token;
                    setCsrfToken(newCsrfToken);
                } catch (csrfError) {
                    console.error("Logged in, but failed to fetch CSRF token on reload:", csrfError);
                    setUser(null);
                    setIsLoggedIn(false);
                }

            } catch (error) {
                console.log("Initialization failed: User is not logged in.", error.response?.data);
                setUser(null);
                setIsLoggedIn(false);
                setCsrfToken(null);
            } finally {
                setIsLoading(false);
            }
        };

        initializeAuth();
    }, []);

    const login = async (loginUserData, csrfToken) => {
        try {
            setCsrfToken(csrfToken);

            const profileResponse = await apiClient.get('/users/profile/me');
            const fullUserData = profileResponse.data;

            setUser(fullUserData);
            setIsLoggedIn(true);
        } catch (error) {
            console.error("Failed to fetch full profile after login, using basic info.", error);
            setUser(loginUserData);
            setIsLoggedIn(true);
        }
    };

    const logout = async (navigate) => {
        try {
            await apiClient.post('/auth/logout');
            console.log("Logout API call successful.");
        } catch (error) {
            console.error("Logout failed, but clearing client-side state anyway.", error);
        } finally {
            setUser(null);
            setIsLoggedIn(false);
            setCsrfToken(null);

            if(navigate){
                navigate('/guest');
            } else {
                window.location.href = '/guest';
            }
        }
    };

    const value = {
        user,
        setUser,
        isLoggedIn,
        isLoading,
        login,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};