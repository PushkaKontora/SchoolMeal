import AsyncStorage from '@react-native-async-storage/async-storage';
import jwtDecode from 'jwt-decode';

export const JwtManager = {
  async getToken(tokenKey: string): Promise<string | null> {
    try {
      return await AsyncStorage.getItem(tokenKey);
    } catch (e: any) {
      throw new Error(e.message);
    }
  },

  async saveToken(tokenKey: string, tokenValue: string) {
    try {
      await AsyncStorage.setItem(tokenKey, tokenValue);
    } catch (e: any) {
      throw new Error(e.message);
    }
  },

  async dropToken(tokenKey: string) {
    try {
      await AsyncStorage.removeItem(tokenKey);
    } catch (e: any) {
      throw new Error(e.message);
    }
  },

  decodeToken(token?: string | null): any {
    if (!token) {
      return null;
    }

    return jwtDecode(token);
  }
};
