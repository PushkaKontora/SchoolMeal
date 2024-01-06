import {ToastProvider} from 'react-native-toast-notifications';
import {ToastNotifierProps} from '../model/props';
import {CONFIG} from '../config/config';

export function ToastNotifier(props: ToastNotifierProps) {
  return (
    <ToastProvider
      {...CONFIG}
      {...props}>
      {props.children}
    </ToastProvider>
  );
}
