import {ValueBadgeProps} from './props.ts';

export function showDash(value: ValueBadgeProps['value']): boolean {
  return Boolean(value && Number(value) > 0);
}
