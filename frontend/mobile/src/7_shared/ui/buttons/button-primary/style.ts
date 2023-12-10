import {StyleSheet} from 'react-native';
import {ButtonPrimaryProps} from './props';

export const createStyle = (props: ButtonPrimaryProps) => StyleSheet.create({
  default: {
    borderRadius: props.borderRadius || 10,
    backgroundColor: props.backgroundColor || '#2C2C2C',
    paddingVertical: props.paddingVertical || 8.5,
    paddingHorizontal: props.paddingHorizontal || 0,
    width: '100%',
    alignItems: 'center',
    flex: props.flex
  },
  disabled: {
    opacity: 0.75
  },
  title: {
    color: props.textColor || '#FFFFFF',
    fontWeight: props.fontWeight || '600',
    fontSize: props.fontSize || 16
  }
});
