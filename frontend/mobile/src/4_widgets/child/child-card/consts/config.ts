import {MealPlanStatus} from '../../../../6_entities/child';

export const MealStatusColors: {[index: string]: string} = {
  [MealPlanStatus.Preferential]: '#4941C4',
  [MealPlanStatus.NotFeeding]: '#909090',
  [MealPlanStatus.Paid]: '#51B078'
};
