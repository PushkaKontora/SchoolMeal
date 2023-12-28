import {PeriodDateBadgeProps} from '../model/props';
import {createPeriodBadgeStyles} from '../const/styles/period-badge-styles';
import {Text, View} from 'react-native';
import {transformDateToString} from '../lib/period-badge';

import {equalsDates} from '../../../../../lib/date/lib/utils';

export function PeriodDateBadge(props: PeriodDateBadgeProps) {
  const styles = createPeriodBadgeStyles();

  const transformDate = props.transformDateToString || transformDateToString;

  const isEqualDates = () => {
    if (props.endingDate) {
      return equalsDates(props.startingDate, props.endingDate);
    }
    return false;
  };

  return (
    <View style={styles.container}>
      <View style={styles.badge}>
        <Text style={styles.text}>
          {transformDate(props.startingDate)}
        </Text>
        {
          (props.endingDate && !isEqualDates()) &&
            <Text style={styles.text}>
                &#10132;
            </Text>
        }
        {
          (props.endingDate && !isEqualDates()) &&
            <Text style={styles.text}>
              {transformDate(props.endingDate)}
            </Text>
        }
      </View>
    </View>
  );
}