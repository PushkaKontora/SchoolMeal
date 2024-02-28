import {CSSProperties, PropsWithChildren} from 'react';

export type AbstractCellStyles = {
  width?: CSSProperties['width'];
  minWidth?: CSSProperties['minWidth'];
  maxWidth?: CSSProperties['maxWidth'];
  whiteSpace?: CSSProperties['whiteSpace'];
  height?: CSSProperties['height'];
  backgroundColor?: CSSProperties['backgroundColor'];
  fontFamily?: CSSProperties['fontFamily'];
  justifyContext?: CSSProperties['justifyContent'];
}

export type AbstractCellProps = PropsWithChildren
  & {
  key: string;
  header?: boolean;
  as?: string;
  cellStyles?: AbstractCellStyles
};
