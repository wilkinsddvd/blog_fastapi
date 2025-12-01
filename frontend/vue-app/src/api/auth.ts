import api from './axios';

export function login(username: string, password: string) {
  return api.post('/auth/login', { username, password });
}

export function register(payload: {
  username: string, email: string, phone: string, password: string
}) {
  return api.post('/auth/register', payload);
}

export function requestPasswordReset(phone: string) {
  return api.post('/auth/request_password_reset', phone, {
    headers: { "Content-Type": "application/json" }
  });
}

export function resetPassword(phone: string, code: string, newPassword: string) {
  return api.post('/auth/reset_password', { phone, code, new_password: newPassword });
}

export function logout() {
  return api.post('/auth/logout');
}