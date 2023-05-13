const AUTHORIZATION = 'Authorization';

export function addAuthHeader(headers: Headers, token: string): Headers {
  headers.set(AUTHORIZATION, `Bearer ${token}`);

  return headers;
}
