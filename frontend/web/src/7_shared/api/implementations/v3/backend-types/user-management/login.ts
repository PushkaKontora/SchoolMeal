import {Fingerprint} from './fingerprint.ts';
import {AccessTokenOut} from './access-token-out.ts';

export type LoginBody = {
  login: string,
  password: string
} & Fingerprint;

export type LoginResponse = AccessTokenOut;
