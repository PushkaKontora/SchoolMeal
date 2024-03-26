import {Fingerprint} from './fingerprint.ts';
import {AccessTokenOut} from './access-token-out.ts';

export type RefreshBody = Fingerprint;

export type RefreshResponse = AccessTokenOut;
