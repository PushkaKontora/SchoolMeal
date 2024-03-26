import jwtDecode from 'jwt-decode';

/**
 * @deprecated
 */
// TODO: создать модуль Storage вместо этого
export const getToken = (tokenKey: string): string => {
  const token = localStorage.getItem(tokenKey);
  return token;
};

/**
 * @deprecated
 */
export const saveToken = (tokenKey: string, token: string): void => {
  localStorage.setItem(tokenKey, token);
};

/**
 * @deprecated
 */
export const dropToken = (tokenKey: string): void => {
  localStorage.removeItem(tokenKey);
};

/**
 * @deprecated
 */
export const decodeToken = (tokenKey: string): any => {
  const token = getToken(tokenKey);

  if (!token) {
    return undefined;
  }

  return jwtDecode(token);
};
