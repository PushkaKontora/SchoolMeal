import {PropsWithChildren} from 'react';

export type ContentStyles = {
  width?: string
}

export type ContentProps = ContentStyles &
  PropsWithChildren;
