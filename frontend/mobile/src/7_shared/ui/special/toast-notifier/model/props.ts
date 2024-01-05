import {ComponentProps} from 'react';
import {ToastProvider} from 'react-native-toast-notifications';
import {ToastProps} from 'react-native-toast-notifications/lib/typescript/toast';

export type ToastNotifierProps = ComponentProps<typeof ToastProvider>;

export type ToastPayload = {
  title?: string,
  description?: string
};

export type TypedToastProps = ToastProps & {
  data?: ToastPayload
};
