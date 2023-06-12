import jwtDecode from 'jwt-decode';

export const getToken = (tokenKey: string): string => {
  const token = localStorage.getItem(tokenKey);
  return token;
};

export const saveToken = (tokenKey: string, token: string): void => {
  localStorage.setItem(tokenKey, token);
};

export const dropToken = (tokenKey: string): void => {
  localStorage.removeItem(tokenKey);
};

export const decodeToken = (tokenKey: string): any => {
  const token = getToken(tokenKey);

  if (!token) {
    return undefined;
  }

  return jwtDecode(token);
};
