import {Text, View} from 'react-native';
import {ToggleButton} from '../../../7_shared/ui/buttons/toggle-button';
import {styles} from './styles';
import {NutritionHeaderFeatureProps} from './props';
import {getFullName} from '../../../6_entities/child/lib/child-utils';

export function NutritionHeaderFeature(props: NutritionHeaderFeatureProps) {
  return (
    <View
      style={styles.container}>

      {
        props.child &&
        <Text
          style={styles.title}>
          {getFullName(props.child)}
        </Text>
      }

      <View style={styles.toggleView}>
        <ToggleButton
          leftTitle={'Не питается'}
          rightTitle={'Питается'}
          defaultState={props?.defaultToggleState}
          onToggle={props.onToggle}/>
      </View>
    </View>
  );
}
