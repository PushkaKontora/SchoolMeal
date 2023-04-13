import {PropsWithChildren} from 'react';

export type Paddings = {
  padding?: number,
  paddingTop?: number,
  paddingLeft?: number,
  paddingBottom?: number,
  paddingRight?: number,
  paddingVertical?: number,
  paddingHorizontal?: number,
}

export type PaddingAreaProps = PropsWithChildren & Paddings;
