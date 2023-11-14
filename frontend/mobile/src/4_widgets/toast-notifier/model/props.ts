import {ComponentProps} from 'react';
import {ToastProvider} from 'react-native-toast-notifications';
import {ToastProps} from 'react-native-toast-notifications/lib/typescript/toast';

export type ToastNotifierProps = ComponentProps<typeof ToastProvider>;

export type TypedToastProps = ToastProps & {
  data?: {
    title: string,
    description: string
  }
};
