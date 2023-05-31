export type NutritionTogglesFeatureProps = {
  onToggleBreakfast: (turnedOn: boolean) => void,
  onToggleLunch: (turnedOn: boolean) => void,
  onToggleAfternoonSnack: (turnedOn: boolean) => void,
  breakfastState?: boolean,
  lunchState?: boolean,
  afternoonSnackState?: boolean,
  hasBreakfast: boolean,
  hasLunch: boolean,
  hasAfternoonSnack: boolean
}
