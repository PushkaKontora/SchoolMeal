import {View, Text} from 'react-native';
import {NutritionCertFeatureProps} from './props';
import {styles} from './styles';
import {formatDateToCasual} from '../../../7_shared/lib/date';

export function NutritionCertFeature(props: NutritionCertFeatureProps) {
  return (
    <View
      style={styles.container}>
      {
        props.nutritionInfo?.preferentialCertificate &&
        <View>
          <Text
            style={styles.title}>
            {'Справка действительна до'}
          </Text>

          <Text
            style={styles.dateBadge}>
            {
              formatDateToCasual(new Date(props.nutritionInfo.preferentialCertificate.endsAt))
            }
          </Text>
        </View>
      }
    </View>
  );
}
