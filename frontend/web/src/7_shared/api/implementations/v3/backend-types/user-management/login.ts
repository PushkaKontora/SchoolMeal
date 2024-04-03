import {FingerprintOut} from './fingerprintOut.ts';
import {AccessTokenOut} from './access-token-out.ts';

export type LoginBody = {
  login: string,
  password: string
} & FingerprintOut;

export type LoginResponse = AccessTokenOut;
