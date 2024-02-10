import {AbstractCellProps} from '../../../../7_shared/ui/v2/table';

export type BadgeProps = {
  text: string
};

export type BadgeCellProps = AbstractCellProps
  & BadgeProps
  & {
  cancelled: boolean
};
