import {Child} from '../../../6_entities/child/model/child';

export type NutritionHeaderFeatureProps = {
  child?: Child,
  onToggle: (turnedOn: boolean) => void,
  defaultToggleState?: boolean
};
