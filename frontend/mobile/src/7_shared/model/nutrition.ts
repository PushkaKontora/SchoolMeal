import {UUID} from './uuid';

export type PupilNutritionInfo = {
  id: UUID,
  lastName: string,
  firstName: string,
  mealPlan: NutritionPlan,
  preferentialCertificate?: NutritionCertificate,
  cancellationPeriods: CancellationPeriod[],
  status: string
}

export type NutritionPlan = {
  hasBreakfast: boolean,
  hasDinner: boolean,
  hasSnacks: boolean
}

export type NutritionCertificate = {
  endsAt: string
}

export type CancellationPeriod = {
  startsAt: string,
  endsAt: string,
  reasons: string[]
}
