import {ToastNotifierProps} from '../model/props';
import {ToastProps} from 'react-native-toast-notifications/lib/typescript/toast';
import {ToastView} from '../ui/toast-view';
import {COLORS} from './colors';

export const CONFIG: Omit<ToastNotifierProps, 'children'> = {
  placement: 'top',
  duration: 5000,
  animationType: 'slide-in',
  animationDuration: 500,
  successColor: COLORS.success,
  dangerColor: COLORS.danger,
  offsetTop: 40,
  offset: 16,
  swipeEnabled: false,
  renderToast: (toast: ToastProps): JSX.Element => (
    <ToastView {...toast} />
  )
};
