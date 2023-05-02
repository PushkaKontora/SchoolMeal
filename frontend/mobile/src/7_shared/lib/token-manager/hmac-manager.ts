import {HMAC_DEFAULT_ALGORITHM} from './config/config';
import CryptoJS from 'crypto-js';

export const HmacManager = {
  getHash(message: string, passphrase: string) {
    return CryptoJS.HmacSHA256(message, passphrase);
  },

  getProgressiveHash(messages: Array<string>, passphrase: string) {
    const hmac = CryptoJS.algo.HMAC.create(HMAC_DEFAULT_ALGORITHM, passphrase);

    messages
      .forEach(
        (item) => hmac.update(item));

    return hmac.finalize();
  }
};
