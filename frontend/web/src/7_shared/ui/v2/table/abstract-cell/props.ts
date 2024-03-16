import {CSSProperties, PropsWithChildren} from 'react';

export type AbstractCellStyles = {
  width?: CSSProperties['width'];
  minWidth?: CSSProperties['minWidth'];
  maxWidth?: CSSProperties['maxWidth'];
  whiteSpace?: CSSProperties['whiteSpace'];
  height?: CSSProperties['height'];
  backgroundColor?: CSSProperties['backgroundColor'];
  fontFamily?: CSSProperties['fontFamily'];
  justifyContent?: CSSProperties['justifyContent'];
}

export type AbstractCellProps = PropsWithChildren
  & {
  key: string;
  header?: boolean;
  as?: string;
  showContent?: boolean;
  cellStyles?: AbstractCellStyles,
  columnSpan?: number,
  rowSpan?: number
};
