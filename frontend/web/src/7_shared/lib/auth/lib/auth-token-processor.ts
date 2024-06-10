import {AUTH_TOKEN_NAME} from '../config/config.ts';
import {JwtPayload} from '../model/jwt-payload.ts';
import jwtDecode from 'jwt-decode';

// TODO: создать модуль Storage для localStorage
export const AuthTokenProcessor = {
  getAuthToken() {
    return localStorage.getItem(AUTH_TOKEN_NAME);
  },

  decodeAuthToken(token: string | null): JwtPayload | null {
    if (token)
      return jwtDecode(token) as JwtPayload;
    return null;
  },

  getAndDecodeAuthToken(): JwtPayload | null {
    const token = localStorage.getItem(AUTH_TOKEN_NAME);

    return this.decodeAuthToken(token);
  },

  saveAuthToken(token: string) {
    localStorage.setItem(AUTH_TOKEN_NAME, token);
  },

  deleteAuthToken() {
    localStorage.removeItem(AUTH_TOKEN_NAME);
  },

  isTokenExpired(payload: JwtPayload | null) {
    if (payload == null)
      return true;

    return new Date(Date.now()) >= new Date(payload.exp * 1000);
  }
};
