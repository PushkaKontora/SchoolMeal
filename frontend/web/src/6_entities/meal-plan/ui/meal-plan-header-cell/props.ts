import {AbstractCellProps} from '../../../../7_shared/ui/v2/table';

export type MealPlanHeaderCellProps = {
  title: string,
  price: number
} & Omit<AbstractCellProps, 'header'>;
