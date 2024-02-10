import {CSSProperties} from 'react';

export type ButtonPrimaryShadowedStyles = {
    $borderRadius?: string,
    $backgroundColor?: string
    $textColor?: string,
    $fontSize?: string,
    $fontFamily?: CSSProperties['fontFamily'],
    $paddingVertical?: string,
    $paddingHorizontal?: string
}

export type ButtonPrimaryStyles = {
    borderRadius?: string,
    backgroundColor?: string
    textColor?: string,
    fontSize?: string,
    fontFamily?: CSSProperties['fontFamily'],
    paddingVertical?: string,
    paddingHorizontal?: string
}

export type ButtonPrimaryProps =
  ButtonPrimaryStyles & {
    title: string,
    onPress: () => void,
    disabled?: boolean,
  };
