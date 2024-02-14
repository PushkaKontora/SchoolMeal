import {MealRequestStatus} from './meal-request-status.ts';
import {PupilWithPlan} from './pupil.ts';

export type LegacyRequestReportSchoolClass = {
  id: string,
  initials: string,
  breakfast: LegacyRequestReportMealInfo,
  dinner: LegacyRequestReportMealInfo,
  snacks: LegacyRequestReportMealInfo
};

export type LegacyRequestReportMealInfo = {
  paid: number,
  preferential: number,
  total: number
};

export type RequestPlanReport = {
  classId: string,
  onDate: string,
  status: MealRequestStatus,
  pupils: PupilWithPlan[]
}
