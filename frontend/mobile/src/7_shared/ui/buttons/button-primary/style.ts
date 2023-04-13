import {StyleSheet} from 'react-native';
import {ButtonPrimaryProps} from './props';

export const createStyle = (props: ButtonPrimaryProps) => StyleSheet.create({
  default: {
    borderRadius: props.borderRadius || 10,
    backgroundColor: props.backgroundColor || '#2C2C2C',
    paddingVertical: 8.5,
    width: '100%',
    flex: 1,
    alignItems: 'center',

  },
  disabled: {
    opacity: 0.75
  },
  title: {
    color: props.textColor || '#FFFFFF',
    fontWeight: '600',
    fontSize: 16
  }
});
