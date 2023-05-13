import {AUTH_TOKEN_NAME} from '../config/config';
import {JwtManager, HmacManager} from '../../../7_shared/lib/token-manager';
import {TokenPayload} from '../model/token';
import Config from 'react-native-config';

export const AuthTokenService = {
  async getToken() {
    return await JwtManager.getToken(AUTH_TOKEN_NAME);
  },

  async decodeAuthToken(): Promise<TokenPayload> {
    const token = await JwtManager.getToken(AUTH_TOKEN_NAME);

    return JwtManager.decodeToken(token) as TokenPayload;
  },

  async saveAuthToken(token: TokenPayload) {
    await JwtManager.saveToken(AUTH_TOKEN_NAME, token.accessToken);
  },

  async deleteToken() {
    await JwtManager.dropToken(AUTH_TOKEN_NAME);
  },

  async isAuthTokenExpired(decodedToken: TokenPayload) {
    // WIP
    //return (decodedToken.exp.getMilliseconds() - Date.now()) < 0;
  },

  getHmacToken(): string {
    const token = Config?.HMAC_KEY_NAME;

    if (!token) {
      throw new Error('You must set HMAC key as environment variable');
    }

    return token;
  },

  getHmacSignature(message: string) {
    return HmacManager.getHash(message, this.getHmacToken());
  },

  getHmacProgressiveSignature(messages: Array<string>) {
    return HmacManager.getProgressiveHash(messages, this.getHmacToken());
  }
};


