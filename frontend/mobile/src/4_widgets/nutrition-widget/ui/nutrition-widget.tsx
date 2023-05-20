import {View} from 'react-native';
import {styles} from '../consts/styles';
import {NutritionHeaderFeature} from '../../../5_features/nutrition/nutrition-header-feature';
import {NutritionCertFeature} from '../../../5_features/nutrition/nutrition-cert-feature';
import {NutritionTogglesFeature} from '../../../5_features/nutrition/nutrition-toggles-feature';
import {NutritionPanel} from '../../../5_features/nutrition/nutrition-panel';

export function NutritionWidget() {
  return (
    <View
      style={styles.background}>
      <View
        style={styles.card}>

        <NutritionHeaderFeature
          name={'Адельна Пупкина'}
          onToggle={(turnedOn: boolean) => {return;}}/>

        <NutritionCertFeature date={new Date(Date.now())}/>

        <NutritionTogglesFeature
          onToggleBreakfast={(turnedOn: boolean) => {return;}}
          onToggleLunch={(turnedOn: boolean) => {return;}}
          onToggleAfternoonSnack={(turnedOn: boolean) => {return;}}/>

        <NutritionPanel/>

      </View>
    </View>
  );
}
