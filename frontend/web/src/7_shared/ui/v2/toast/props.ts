import {ToastProps} from 'react-toastify/dist/types';
import {MouseEventHandler} from 'react';

export type CloseButtonProps = {
  onClick: MouseEventHandler
};

export type CustomToastProps = {
  message: string,
  onClose?: () => void,
  toastProps?: ToastProps
}
