import {CSSProperties} from 'react';
import {AbstractCellProps} from '../../abstract-cell';
import {ValueBadgeProps} from '../../../../value-badge';

export type ValueBadgeCellStyles = {
  justifyContent?: CSSProperties['justifyContent'],
  padding?: CSSProperties['padding']
}

export type ValueBadgeCellProps = AbstractCellProps
  & {
  styles?: ValueBadgeCellStyles
  badgeProps?: ValueBadgeProps
}
