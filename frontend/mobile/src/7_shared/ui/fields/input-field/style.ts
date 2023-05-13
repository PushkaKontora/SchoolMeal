import {InputStyle} from './props';
import {StyleSheet} from 'react-native';

export const createStyle = (props?: InputStyle) => StyleSheet.create({
  default: {
    width: props?.width || '100%',
    paddingVertical: props?.paddingVertical || 8,
    paddingHorizontal: props?.paddingHorizontal || 12,
    backgroundColor: props?.backgroundColor || '#F2F2F2',
    borderRadius: props?.borderRadius || 10,
    borderColor: props?.borderColor,
    borderWidth: props?.borderWidth,
    color: props?.color || '#151515'
  }
});
