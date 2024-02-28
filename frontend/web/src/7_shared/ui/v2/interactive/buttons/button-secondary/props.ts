import {CSSProperties} from 'react';

export type ButtonSecondaryStyles = {
  borderRadius?: string,
  backgroundColor?: string
  textColor?: string,
  fontSize?: string,
  paddingVertical?: string,
  paddingHorizontal?: string,
  width?: CSSProperties['width'],
  height?: CSSProperties['height']
}

export type ButtonSecondaryProps =
  ButtonSecondaryStyles & {
  title: string,
  onPress: () => void,
  disabled?: boolean,
};