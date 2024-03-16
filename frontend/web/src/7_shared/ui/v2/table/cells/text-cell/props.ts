import {CSSProperties} from 'react';
import {AbstractCellProps} from '../../abstract-cell';

export type TextCellStyles = {
  justifyContent?: CSSProperties['justifyContent'];
  padding?: CSSProperties['padding']
};

export type TextCellProps = AbstractCellProps
  & {
  styles?: TextCellStyles,
  text: string
};