export type MealPlanViewData = {
  paid: number,
  preferential: number,
  total: number
}

export type MealRequestRowViewData = {
  schoolClass: string,
  breakfast: MealPlanViewData,
  dinner: MealPlanViewData,
  snacks: MealPlanViewData
}
