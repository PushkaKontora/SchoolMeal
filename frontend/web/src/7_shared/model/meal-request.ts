export type MealRequest = {
  school_classes: MealRequestSchoolClass[],
  paid_total: number,
  preferential_total: number,
  total: number
};

export type MealRequestSchoolClass = {
  id: string,
  initials: string,
  breakfast: MealRequestMealPlan,
  dinner: MealRequestMealPlan,
  snacks: MealRequestMealPlan
};

export type MealRequestMealPlan = {
  paid: number,
  preferential: number,
  total: number
}
