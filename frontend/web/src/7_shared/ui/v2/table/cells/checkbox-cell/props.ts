import {AbstractCellProps} from '../../abstract-cell';
import {CheckboxProps} from '../../../interactive/check-box';
import {CSSProperties} from 'react';

export type CheckboxCellStyles = {
  justifyContent?: CSSProperties['justifyContent']
}

export type CheckboxCellProps = AbstractCellProps
  & CheckboxProps
  & {
  styles?: CheckboxCellStyles
};
