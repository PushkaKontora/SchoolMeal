import {NutritionTogglesFeatureProps} from './props';
import {Text, View} from 'react-native';
import {styles} from './styles';
import {Switch} from '../../../7_shared/ui/buttons/switch/switch';

export function NutritionTogglesFeature(props: NutritionTogglesFeatureProps) {
  return (
    <View
      style={styles.container}>

      {
        props.hasBreakfast && (
          <View
            style={styles.field}>
            <Text
              style={styles.label}>
              {'Завтрак'}
            </Text>

            <Switch
              onToggle={props.onToggleBreakfast}
              defaultState={props.breakfastState}/>
          </View>
        )
      }

      {
        props.hasLunch && (
          <View
            style={styles.field}>
            <Text
              style={styles.label}>
              {'Обед'}
            </Text>

            <Switch
              onToggle={props.onToggleLunch}
              defaultState={props.lunchState}/>
          </View>
        )
      }

      {
        props.hasAfternoonSnack && (
          <View
            style={styles.field}>
            <Text
              style={styles.label}>
              {'Полдник'}
            </Text>

            <Switch
              onToggle={props.onToggleAfternoonSnack}
              defaultState={props.afternoonSnackState}/>
          </View>
        )
      }

    </View>
  );
}
