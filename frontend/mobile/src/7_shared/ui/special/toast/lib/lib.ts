import {TypedToastProps} from '../model/props';
import {COLORS} from '../config/colors';

export function setBackgroundColor(type: TypedToastProps['type']) {
  if (type) {
    return COLORS[type];
  }

  return COLORS['success'];
}
