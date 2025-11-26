import React, { createContext, useState, useContext, useEffect} from "react";
import apiClient from '../api/apiClient';

const AuthContext = createContext(null);
export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const checkUserStatus = async () => {
            try {
                const response = await apiClient.get('/users/profile/me');
                setUser(response.data);
                setIsLoggedIn(true);
            } catch (error) {
                console.log("User is not logged in.", error.response?.data);
                setUser(null);
                setIsLoggedIn(false);
            } finally {
                setIsLoading(false);
            }
        };
        
        checkUserStatus();
    }, []);

    const login = (userData) => {
        setUser(userData);
        setIsLoggedIn(true);
    };

    const logout = async () => {
        try {
            await apiClient.post('/auth/logout');
        } catch (error) {
            console.error("Logout failed, but clearing client-side state anyway.", error);
        } finally {
            setUser(null);
            setIsLoggedIn(false);
        }
    };

    const value = {
        user,
        setUser, // Cung cấp cả setUser để ProfilePage có thể cập nhật
        isLoggedIn,
        isLoading, // Rất quan trọng để tránh "nháy" giao diện
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
