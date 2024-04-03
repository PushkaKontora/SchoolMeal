import {FingerprintOut} from './fingerprintOut.ts';
import {AccessTokenOut} from './access-token-out.ts';

export type RefreshBody = FingerprintOut;

export type RefreshResponse = AccessTokenOut;
