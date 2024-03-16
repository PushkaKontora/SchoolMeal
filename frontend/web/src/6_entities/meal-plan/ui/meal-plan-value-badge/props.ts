import {ValueBadgeProps} from '../../../../7_shared/ui/v2/value-badge';
import {StyleTypes} from './const.ts';
import {AbstractCellProps} from '../../../../7_shared/ui/v2/table';
import {CSSProperties} from 'react';

export type MealPlanValueBadgeStyles = {
  justifyContent?: CSSProperties['justifyContent'];
  padding?: CSSProperties['padding']
};

export type MealPlanValueBadgeProps = {
  value: ValueBadgeProps['value'],
  type?: ValueBadgeProps['type'] | StyleTypes,
  styles?: MealPlanValueBadgeStyles
} & Omit<AbstractCellProps, 'header'>;
