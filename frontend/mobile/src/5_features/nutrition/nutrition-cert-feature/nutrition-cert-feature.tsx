import {View, Text} from 'react-native';
import {NutritionCertFeatureProps} from './props';
import {styles} from './styles';
import {formatDateToCasual} from '../../../7_shared/lib/date';

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
            {formatDateToCasual(new Date(props.child.certificateBeforeDate))}
          </Text>
        </View>
      }
    </View>
  );
}
