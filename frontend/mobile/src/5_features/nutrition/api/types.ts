import {NutritionPlan} from '../../../7_shared/model/nutrition';

export type ChangeNutritionPlanIn = {
  pupilId: string,
  body: NutritionPlan
}

export type CancelNutritionIn = {
  pupilId: string,
  body: {
    startsAt: string,
    endsAt: string,
    reason?: string
  }
}

export type ResumeNutritionIn = {
  pupilId: string,
  body: {
    date: string
  }
}
