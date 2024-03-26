/**
 * @deprecated
 */
export type MealRequest = {
  school_classes: MealRequestSchoolClass[],
  paid_total: number,
  preferential_total: number,
  total: number
};

/**
 * @deprecated
 */
export type MealRequestSchoolClass = {
  id: string,
  initials: string,
  breakfast: MealRequestMealPlan,
  dinner: MealRequestMealPlan,
  snacks: MealRequestMealPlan
};

/**
 * @deprecated
 */
export type MealRequestMealPlan = {
  paid: number,
  preferential: number,
  total: number
}
