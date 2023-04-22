import {PaddingAreaProps} from './props';
import {StyleSheet} from 'react-native';

export const createStyle = (props: PaddingAreaProps) => StyleSheet.create({
  default: {
    ...props
  }
});