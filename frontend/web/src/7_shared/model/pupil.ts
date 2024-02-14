import {UUID} from './uuid.ts';
import {MealPlan} from './meal-plan.ts';
import {CancellationPeriod} from './cancellation-period.ts';
import {MealRequestStatus} from './meal-request-status.ts';

export type Pupil = {
  id: UUID,
  lastName: string,
  firstName: string,
  mealPlan: MealPlan,
  preferentialCertificate: {
    endsAt: string
  },
  cancellationPeriods: CancellationPeriod[],
  status: MealRequestStatus
}

export type PupilWithPlan = {
  id: UUID,
  last_name: string,
  first_name: string,
  patronymic: string,
  breakfast: boolean,
  dinner: boolean,
  snacks: boolean
}

export type OverridenPupil = {
  id: string,
  breakfast: boolean,
  dinner: boolean,
  snacks: boolean
}
