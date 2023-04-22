import AsyncStorage from '@react-native-async-storage/async-storage';
import jwtDecode from 'jwt-decode';

export async function getToken(tokenKey: string): Promise<string | null> {
  try {
    return await AsyncStorage.getItem(tokenKey);
  } catch (e: any) {
    throw new Error(e.message);
  }
}

export async function saveToken(tokenKey: string, tokenValue: string) {
  try {
    await AsyncStorage.setItem(tokenKey, tokenValue);
  } catch (e: any) {
    throw new Error(e.message);
  }
}

export async function dropToken(tokenKey: string) {
  try {
    await AsyncStorage.removeItem(tokenKey);
  } catch (e: any) {
    throw new Error(e.message);
  }
}

export function decodeToken(token?: string | null): any {
  if (!token) {
    return null;
  }

  return jwtDecode(token);
}
