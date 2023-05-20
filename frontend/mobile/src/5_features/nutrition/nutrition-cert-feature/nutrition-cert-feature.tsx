import {View, Text} from 'react-native';
import {NutritionCertFeatureProps} from './props';
import {styles} from './styles';
import {formatDate} from '../../../6_entities/date';

export function NutritionCertFeature(props: NutritionCertFeatureProps) {
  return (
    <View
      style={styles.container}>
      <Text
        style={styles.title}>
        {'Справка действительна до'}
      </Text>

      <Text
        style={styles.dateBadge}>
        {formatDate(props.date)}
      </Text>
    </View>
  );
}
