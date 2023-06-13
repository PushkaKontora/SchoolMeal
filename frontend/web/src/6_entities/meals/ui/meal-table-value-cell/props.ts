export type MealTableValueCellStyles = {
  backgroundColor?: string,
  borderRadius?: string
}

export type MealTableValueCellProps = {
  paid: string,
  preferential: string,
  total: string
} & MealTableValueCellStyles;
