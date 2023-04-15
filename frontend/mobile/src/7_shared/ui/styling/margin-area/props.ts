import {PropsWithChildren} from 'react';

export type Margins = {
  margin?: number,
  marginTop?: number,
  marginLeft?: number,
  marginBottom?: number,
  marginRight?: number,
  marginVertical?: number,
  marginHorizontal?: number,
}

export type MarginAreaProps = {
  style?: any
} & PropsWithChildren & Margins;