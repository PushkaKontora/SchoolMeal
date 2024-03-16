import {Table} from '@tanstack/react-table';
import {CSSProperties} from 'react';

export type TableStyles = {
  width?: CSSProperties['width']
}

export type ReactTableWrapperProps<T> = {
  table: Table<T>,
  styles?: TableStyles,
  footerAtTop?: boolean
}
