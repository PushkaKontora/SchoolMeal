import {AUTH_TOKEN_NAME} from './config/config';
import * as JwtManager from '../../7_shared/lib/token-manager';
import {TokenPayload} from './model/token';

export async function decodeAuthToken(): Promise<TokenPayload> {
  const token = await JwtManager.getToken(AUTH_TOKEN_NAME);

  return JwtManager.decodeToken(token) as TokenPayload;
}

export async function isAuthTokenExpired(decodedToken: TokenPayload) {
  return (decodedToken.exp.getMilliseconds() - Date.now()) < 0;
}

export function getHmacToken() {
  return process.env.HMAC_KEY_NAME;
}
