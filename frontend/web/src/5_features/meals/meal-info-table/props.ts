import {MealCellData} from './types';

export type MealInfoTableStyles = {
  width: string
}

export type MealInfoTableProps = {
  showMissingValues: boolean,
  data: MealCellData[],
  title: string
} & MealInfoTableStyles;
