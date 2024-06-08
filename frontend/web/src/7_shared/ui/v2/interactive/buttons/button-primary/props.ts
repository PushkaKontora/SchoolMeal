import {CSSProperties} from 'react';

export type ButtonPrimaryShadowedStyles = {
    $borderRadius?: CSSProperties['borderRadius'],
    $backgroundColor?: string
    $textColor?: string,
    $fontSize?: CSSProperties['fontSize'],
    $fontFamily?: CSSProperties['fontFamily'],
    $paddingVertical?: string,
    $paddingHorizontal?: string,
    $width?: CSSProperties['width'],
    $height?: CSSProperties['height'],
    $flex?: CSSProperties['flex']
}

export type ButtonPrimaryStyles = {
    borderRadius?: CSSProperties['borderRadius'],
    backgroundColor?: CSSProperties['backgroundColor'],
    textColor?: CSSProperties['color'],
    fontSize?: CSSProperties['fontSize'],
    fontFamily?: CSSProperties['fontFamily'],
    paddingVertical?: string,
    paddingHorizontal?: string,
    width?: CSSProperties['width']
    height?: CSSProperties['height'],
    flex?: CSSProperties['flex']
}

export type ButtonPrimaryProps =
  ButtonPrimaryStyles & {
    title: string,
    onPress: () => void,
    disabled?: boolean,
  };
