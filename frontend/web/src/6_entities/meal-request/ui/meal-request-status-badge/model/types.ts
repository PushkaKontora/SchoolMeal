import {CSSProperties} from 'react';

export type StatusValue<K extends string | number | symbol> = {
  [key in K]: {
    name: string;
    color: CSSProperties['color'];
  };
};
