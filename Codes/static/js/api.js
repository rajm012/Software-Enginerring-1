// API Helper Functions
import API_CONFIG from './config.js';

class API {
    static async request(endpoint, options = {}) {
        try {
            const url = API_CONFIG.baseURL + endpoint;
            const config = {
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            };

            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            throw error;
        }
    }

    // Auth APIs
    static async register(userData) {
        return this.request(API_CONFIG.endpoints.register, {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    static async registerAdmin(userData) {
        return this.request(API_CONFIG.endpoints.registerAdmin, {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    static async login(credentials) {
        return this.request(API_CONFIG.endpoints.login, {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
    }

    static async logout() {
        return this.request(API_CONFIG.endpoints.logout, {
            method: 'POST'
        });
    }

    static async getCurrentUser() {
        return this.request(API_CONFIG.endpoints.me);
    }

    static async forgotPassword(email) {
        return this.request(API_CONFIG.endpoints.forgotPassword, {
            method: 'POST',
            body: JSON.stringify({ email })
        });
    }

    static async verifyOtp(email, otp) {
        return this.request(API_CONFIG.endpoints.verifyOtp, {
            method: 'POST',
            body: JSON.stringify({ email, otp })
        });
    }

    static async resetPassword(email, otp, new_password) {
        return this.request(API_CONFIG.endpoints.resetPassword, {
            method: 'POST',
            body: JSON.stringify({ email, otp, new_password })
        });
    }

    static async changePassword(currentPassword, newPassword) {
        return this.request(API_CONFIG.endpoints.changePassword, {
            method: 'POST',
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword
            })
        });
    }

    static async updateLocation(location) {
        return this.request(API_CONFIG.endpoints.updateLocation, {
            method: 'POST',
            body: JSON.stringify({ location })
        });
    }

    // Alert APIs
    static async createAlert(alertData) {
        return this.request(API_CONFIG.endpoints.createAlert, {
            method: 'POST',
            body: JSON.stringify(alertData)
        });
    }

    static async verifyAlert(alertId) {
        return this.request(API_CONFIG.endpoints.verifyAlert(alertId), {
            method: 'POST'
        });
    }

    static async dispatchAlert(alertId) {
        return this.request(API_CONFIG.endpoints.dispatchAlert(alertId), {
            method: 'POST'
        });
    }

    static async getMyAlerts() {
        return this.request(API_CONFIG.endpoints.myAlerts);
    }

    static async getAllAlerts(status = '', page = 1) {
        const params = new URLSearchParams();
        if (status) params.append('status', status);
        params.append('page', page);
        
        return this.request(`${API_CONFIG.endpoints.allAlerts}?${params}`);
    }

    static async getAlertById(alertId) {
        return this.request(API_CONFIG.endpoints.alertById(alertId));
    }

    static async deleteAlert(alertId) {
        return this.request(API_CONFIG.endpoints.deleteAlert(alertId), {
            method: 'DELETE'
        });
    }

    static async getAlertStats() {
        return this.request(API_CONFIG.endpoints.alertStats);
    }

    // Utility APIs
    static async getCities() {
        return this.request(API_CONFIG.endpoints.cities);
    }

    static async getAllUsers() {
        return this.request(API_CONFIG.endpoints.users);
    }
}

export default API;

//
// Credits:
//     Raj: Logic, Code and Idea
//     AI Chatbots: Optimization, Formatting
//

