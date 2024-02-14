import {CSSProperties} from 'react';

export type ButtonPrimaryShadowedStyles = {
    $borderRadius?: string,
    $backgroundColor?: string
    $textColor?: string,
    $fontSize?: string,
    $fontFamily?: CSSProperties['fontFamily'],
    $paddingVertical?: string,
    $paddingHorizontal?: string,
    $width?: CSSProperties['width'],
    $height?: CSSProperties['height']
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
    height?: CSSProperties['height']
}

export type ButtonPrimaryProps =
  ButtonPrimaryStyles & {
    title: string,
    onPress: () => void,
    disabled?: boolean,
  };
