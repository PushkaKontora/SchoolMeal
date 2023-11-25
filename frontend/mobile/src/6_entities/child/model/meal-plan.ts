export type MealPlan = {
  status: MealPlanStatus
}

export enum MealPlanStatus {
  Preferential = 'Питается льготно',
  Paid = 'Питается платно',
  NotFeeding = 'Не питается'
}
