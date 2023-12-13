import {Text, View} from 'react-native';
import {ToggleButton} from '../../../7_shared/ui/buttons/toggle-button';
import {styles} from './styles';
import {NutritionHeaderFeatureProps} from './props';
import {PreferentialBadge} from '../../../7_shared/ui/special/preferential-badge';

export function NutritionHeaderFeature(props: NutritionHeaderFeatureProps) {
  return (
    props.nutritionInfo && (
      <View
        style={styles.container}>

        {
          <Text
            style={styles.title}>
            {`${props.nutritionInfo.firstName} ${props.nutritionInfo.lastName}`}
          </Text>
        }

        <View style={styles.toggleView}>
          {
            props.nutritionInfo?.preferentialCertificate ? (
              <PreferentialBadge title={'Льготное питание'}/>
            ) :
              (
                <ToggleButton
                  leftTitle={'Не питается'}
                  rightTitle={'Питается'}
                  defaultState={props?.defaultToggleState}
                  onToggle={props.onToggle}/>
              )
          }
        </View>
      </View>
    )
  );
}
