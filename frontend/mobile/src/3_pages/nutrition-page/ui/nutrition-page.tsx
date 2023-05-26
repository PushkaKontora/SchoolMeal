import {NutritionWidget} from '../../../4_widgets/nutrition-widget';
import {NutritionPageProps} from '../types/props';
import {useRoute} from '@react-navigation/native';
import {NutritionRouteProp} from '../types/route-props';

export function NutritionPage({navigation}: NutritionPageProps) {
  const route = useRoute<NutritionRouteProp>();
  const {childId} = route.params;

  return (
    <NutritionWidget childId={childId}/>
  );
}
