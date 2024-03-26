import {MealRequestStatus} from './meal-request-status.ts';
import {PupilWithPlan} from './pupil.ts';

/**
 * @deprecated
 */
export type LegacyRequestReportSchoolClass = {
  id: string,
  initials: string,
  breakfast: LegacyRequestReportMealInfo,
  dinner: LegacyRequestReportMealInfo,
  snacks: LegacyRequestReportMealInfo
};

/**
 * @deprecated
 */
export type LegacyRequestReportMealInfo = {
  paid: number,
  preferential: number,
  total: number
};

/**
 * @deprecated
 */
export type RequestPlanReport = {
  classId: string,
  onDate: string,
  status: MealRequestStatus,
  pupils: PupilWithPlan[]
}
