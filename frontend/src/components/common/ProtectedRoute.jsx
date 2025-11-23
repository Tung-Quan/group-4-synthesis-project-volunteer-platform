import React from 'react';
import { Navigate } from 'react-router-dom';

function ProtectedRoute ({ user, allowedRoles, children}) {
    if (allowedRoles && !allowedRoles.includes(user.type)) {
        console.warn(`Access denied: User type '${user.type}' cannot access this page.`);
        return <Navigate to="/" replace />;
    }

    return children; // trang mà muốn đăng nhập vào
}
export default ProtectedRoute;