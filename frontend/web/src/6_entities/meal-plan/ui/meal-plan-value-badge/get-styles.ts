import {Styles, StyleTypes} from './const.ts';

export function getStyles(type?: StyleTypes) {
  return type ? Styles?.[type] : undefined;
}
