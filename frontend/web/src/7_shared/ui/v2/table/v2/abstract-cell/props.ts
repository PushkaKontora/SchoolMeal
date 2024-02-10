import {CSSProperties, PropsWithChildren} from 'react';

export type AbstractCellStyles = {
  width?: CSSProperties['width'];
  minWidth?: CSSProperties['minWidth'];
  maxWidth?: CSSProperties['maxWidth'];
  height?: CSSProperties['height'];
  backgroundColor?: CSSProperties['backgroundColor'];
  fontFamily?: CSSProperties['fontFamily'];
}

export type AbstractCellProps = PropsWithChildren
  & {
  key: string;
  header?: boolean;
  as?: string;
  cellStyles?: AbstractCellStyles
};
