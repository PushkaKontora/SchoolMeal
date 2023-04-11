import {AUTH_TOKEN_NAME} from './config/config';
import {JwtManager, HmacManager} from '../../7_shared/lib/token-manager';
import {TokenPayload} from './model/token';

export async function decodeAuthToken(): Promise<TokenPayload> {
  const token = await JwtManager.getToken(AUTH_TOKEN_NAME);

  return JwtManager.decodeToken(token) as TokenPayload;
}

export async function isAuthTokenExpired(decodedToken: TokenPayload) {
  return (decodedToken.exp.getMilliseconds() - Date.now()) < 0;
}

export function getHmacToken(): string {
  const token = process.env.HMAC_KEY_NAME;

  if (!token) {
    throw new Error('You must set HMAC key as environment variable');
  }

  return token;
}

export function getHmacSignature(message: string) {
  return HmacManager.getHash(message, getHmacToken());
}

export function getHmacProgressiveSignature(messages: Array<string>) {
  return HmacManager.getProgressiveHash(messages, getHmacToken());
}
