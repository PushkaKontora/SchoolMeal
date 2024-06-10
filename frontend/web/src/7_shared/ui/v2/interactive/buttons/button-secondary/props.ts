import {CSSProperties} from 'react';

export type ButtonSecondaryStyles = {
  borderRadius?: CSSProperties['borderRadius'],
  borderColor?: CSSProperties['borderColor']
  backgroundColor?: string
  textColor?: string,
  fontSize?: string,
  paddingVertical?: string,
  paddingHorizontal?: string,
  width?: CSSProperties['width'],
  height?: CSSProperties['height'],
  flex?: CSSProperties['flex']
}

export type ButtonSecondaryProps =
  ButtonSecondaryStyles & {
  title: string,
  onPress: () => void,
  disabled?: boolean,
};