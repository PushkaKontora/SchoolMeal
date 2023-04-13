import {StyleSheet} from 'react-native';
import {MarginAreaProps} from './props';

export const createStyle = (props: MarginAreaProps) => StyleSheet.create({
  default: {
    ...props
  }
});