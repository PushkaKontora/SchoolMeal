import {Child} from '../../../6_entities/child/model/child';

export type NutritionHeaderFeatureProps = {
  child?: Child,
  onToggle: (toggledRight: boolean) => void,
  defaultToggleState?: boolean
};
