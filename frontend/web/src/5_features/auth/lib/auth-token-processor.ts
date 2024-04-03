import {AUTH_TOKEN_NAME} from '../config/config';
import {JwtPayload} from '../model/jwt-payload.ts';
import jwtDecode from 'jwt-decode';

// TODO: создать модуль Storage для localStorage
export const AuthTokenProcessor = {
  getAuthToken() {
    return localStorage.getItem(AUTH_TOKEN_NAME);
  },

  decodeAuthToken(token: string): JwtPayload | null {
    if (token)
      return jwtDecode(token) as JwtPayload;
    return null;
  },

  getAndDecodeAuthToken(): JwtPayload | null {
    const token = localStorage.getItem(AUTH_TOKEN_NAME);

    if (token)
      return jwtDecode(token) as JwtPayload;
    return null;
  },

  saveAuthToken(token: string) {
    localStorage.setItem(AUTH_TOKEN_NAME, token);
  },

  deleteAuthToken() {
    localStorage.removeItem(AUTH_TOKEN_NAME);
  },

  isTokenExpired(payload: JwtPayload) {
    return new Date(Date.now()) >= new Date(payload.exp * 1000);
  }
};
