import {StyleSheet} from 'react-native';
import {ButtonSecondaryProps} from './props';

export const createStyle = (props: ButtonSecondaryProps) => StyleSheet.create({
  default: {
    borderRadius: props.borderRadius || 100,
    borderColor: props.borderColor || '#2C2C2C',
    backgroundColor: '#FFFFFF00',
    borderWidth: 1,
    paddingVertical: 11,
    width: '100%',
    alignItems: 'center',
  },
  disabled: {
    opacity: 0.75
  },
  title: {
    color: props.textColor || '#2C2C2C',
    fontWeight: '500',
    fontSize: 12
  }
});
