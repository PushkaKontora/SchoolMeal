import {HEADERS} from './headers.ts';

export function addAuthHeader(headers: Headers, token: string): Headers {
  headers.set(HEADERS.Authorization, `Bearer ${token}`);

  return headers;
}