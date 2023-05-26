export type ChildMealData = {
  breakfast: boolean,
  lunch: boolean,
  dinner: boolean
}

export type ChildMealDataWithId = {childId: string} & ChildMealData;
