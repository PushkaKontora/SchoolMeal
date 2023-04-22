import {HorizontalLineProps} from './props';
import {StyleSheet} from 'react-native';

export const createStyle = (props: HorizontalLineProps) => StyleSheet.create({
  default: {
    borderBottomColor: props.color || '#E6E6E6',
    borderBottomWidth: props.height || 1,
    width: props.width || '100%'
  }
});
