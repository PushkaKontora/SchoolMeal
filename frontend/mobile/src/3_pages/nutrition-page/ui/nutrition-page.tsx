import {NutritionWidget} from '../../../4_widgets/nutrition-widget';
import {useRoute} from '@react-navigation/native';
import {NutritionRouteProp} from '../types/route-props';

export function NutritionPage() {
  const route = useRoute<NutritionRouteProp>();
  const {childId} = route.params;

  return (
    <NutritionWidget pupilId={childId}/>
  );
}
