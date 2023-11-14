import {StyleSheet} from 'react-native';
import {ToastProps} from 'react-native-toast-notifications/lib/typescript/toast';
import {setBackgroundColor} from '../lib/lib';

export const createStyle = (props: ToastProps) => StyleSheet.create({
  toastContainer: {
    borderRadius: 12,
    backgroundColor: setBackgroundColor(props.type),
    flexDirection: 'row',
    gap: 16,
    width: 304,
    height: 76,
    padding: 16
  },
  textContainer: {
    flexDirection: 'column',
    alignContent: 'center',
    alignItems: 'flex-start'
  },
  title: {
    color: '#000000',
    fontWeight: '500',
    fontSize: 14,
    lineHeight: 20
  },
  description: {
    color: '#000000',
    fontWeight: '300',
    fontSize: 11,
    lineHeight: 24
  }
});
