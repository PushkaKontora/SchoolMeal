import {ValueBadgeProps} from '../../../../../7_shared/ui/v2/value-badge';

export function setBalanceValueBadgeType(value: number): ValueBadgeProps['type'] {
  if (value <= 0) {
    return 'negative';
  }

  return 'positive';
}
