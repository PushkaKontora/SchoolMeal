import {AUTH_TOKEN_NAME} from '../config/config';
import {TokenPayload} from '../model/token-payload';
import {JwtPayload} from '../model/jwt-payload';
import {decodeToken, dropToken, getToken, saveToken} from '../../../7_shared/lib/token-manager';

export const AuthTokenService = {
  async getToken() {
    return getToken(AUTH_TOKEN_NAME);
  },

  async decodeAuthToken(): Promise<TokenPayload> {
    const token = getToken(AUTH_TOKEN_NAME);

    return decodeToken(token) as TokenPayload;
  },

  async saveAuthToken(token: TokenPayload) {
    await saveToken(AUTH_TOKEN_NAME, token.accessToken);
  },

  async deleteToken() {
    await dropToken(AUTH_TOKEN_NAME);
  },

  async isAuthTokenExpired(decodedToken: JwtPayload) {
    return (decodedToken.expires_in - Date.now()) < 0;
  }
};
