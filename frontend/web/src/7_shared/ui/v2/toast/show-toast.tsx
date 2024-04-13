import GreenTick from './assets/green_tick.svg?react';

import {ToastProps} from 'react-toastify/dist/types';
import {toast} from 'react-toastify';
import {TOAST_OPTIONS} from './const.ts';

export function showToast(
  message: string,
  type?: ToastProps['type']
) {
  if (type === 'success') {
    toast.success(
      message,
      {
        ...TOAST_OPTIONS,
        icon: <GreenTick
          width={'24px'}
          height={'24px'}
        />
      }
    );
  }
}
