import {View, Text} from 'react-native';
import {NutritionCertFeatureProps} from './props';
import {styles} from './styles';
import {formatDate} from '../../../6_entities/date';

export function NutritionCertFeature(props: NutritionCertFeatureProps) {
  return (
    <View
      style={styles.container}>
      {
        props?.child?.certificateBeforeDate &&
        <View>
          <Text
            style={styles.title}>
            {'Справка действительна до'}
          </Text>

          <Text
            style={styles.dateBadge}>
            {formatDate(new Date(props.child.certificateBeforeDate))}
          </Text>
        </View>
      }
    </View>
  );
}
