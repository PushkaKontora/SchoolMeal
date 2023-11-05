import {InputStyle} from './props';
import {StyleSheet} from 'react-native';

export const createStyle = (props?: InputStyle) => StyleSheet.create({
  default: {
    width: props?.width || '100%',
    paddingVertical: props?.paddingVertical === undefined ? 8 : 0,
    paddingHorizontal: props?.paddingHorizontal === undefined ? 12 : 0,
    backgroundColor: props?.backgroundColor || '#F2F2F2',
    borderRadius: props?.borderRadius || 10,
    borderColor: props?.borderColor,
    borderWidth: props?.borderWidth,
    color: props?.color || '#151515',
    textAlignVertical: props?.textAlignVertical || 'center'
  }
});
