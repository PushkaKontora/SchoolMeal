import {Text, View} from 'react-native';
import {ToggleButton} from '../../../7_shared/ui/buttons/toggle-button';
import {styles} from './styles';
import {NutritionHeaderFeatureProps} from './props';

export function NutritionHeaderFeature(props: NutritionHeaderFeatureProps) {
  return (
    <View
      style={styles.container}>
      <Text
        style={styles.title}>
        {props.name}
      </Text>

      <View style={styles.toggleView}>
        <ToggleButton
          turnedOffTitle={'Не питается'}
          turnedOnTitle={'Питается'}
          onToggle={props.onToggle}/>
      </View>
    </View>
  );
}
