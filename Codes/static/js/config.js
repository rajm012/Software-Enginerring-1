/* API Configuration */
const API_CONFIG = {
    baseURL: window.location.origin || 'http://localhost:5000',
    endpoints: {
        // Auth endpoints
        register: '/api/auth/register',
        registerAdmin: '/api/auth/register-admin',
        login: '/api/auth/login',
        logout: '/api/auth/logout',
        me: '/api/auth/me',
        forgotPassword: '/api/auth/forgot-password',
        verifyOtp: '/api/auth/verify-otp',
        resetPassword: '/api/auth/reset-password',
        changePassword: '/api/auth/change-password',
        updateLocation: '/api/auth/update-location',
        
        // Alert endpoints
        createAlert: '/api/alerts/create',
        verifyAlert: (id) => `/api/alerts/verify/${id}`,
        dispatchAlert: (id) => `/api/alerts/dispatch/${id}`,
        myAlerts: '/api/alerts/my-alerts',
        allAlerts: '/api/alerts/all',
        alertById: (id) => `/api/alerts/${id}`,
        deleteAlert: (id) => `/api/alerts/${id}`,
        alertStats: '/api/alerts/stats',
        
        // Utility endpoints
        cities: '/api/cities',
        users: '/api/users/all'
    }
};

export default API_CONFIG;


//
// Credits:
//     Raj: Logic, Code and Idea
//     AI Chatbots: Optimization, Formatting
//

