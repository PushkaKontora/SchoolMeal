import {CSSProperties} from 'react';

export type ValueBadgeStyles = {
  backgroundColor?: string,
  textColor?: string,
  width?: string,
  margin?: string,
  fontFamily?: CSSProperties['fontFamily']
}

export type ValueBadgeProps = {
  value?: string,
  type?: 'negative' | 'positive',
  styles?: ValueBadgeStyles
};
