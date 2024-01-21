import {PupilNutritionInfo} from '../../../7_shared/model/nutrition';

export type NutritionHeaderFeatureProps = {
  nutritionInfo?: PupilNutritionInfo,
  onToggle: (toggledRight: boolean) => void,
  defaultToggleState?: boolean
};
