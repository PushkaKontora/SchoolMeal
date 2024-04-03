import {
  NutritionStatus
} from '../../../../../7_shared/api/implementations/v3/frontend-types/nutrition/nutrition-status.ts';

export type TableRowViewData = {
  firstName: string,
  lastName: string,
  patronymic?: string,
  status: NutritionStatus,
  breakfast: boolean,
  dinner: boolean,
  snacks: boolean
};

export type TableViewData = {
  hasBreakfast: boolean,
  hasDinner: boolean,
  hasSnacks: boolean
}
