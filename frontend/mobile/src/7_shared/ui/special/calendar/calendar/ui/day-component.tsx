import {Text, TouchableOpacity, View} from 'react-native';
import {DayComponentProps} from '../model/props';
import {createDayStyle} from '../const/styles/day-styles';
import {memo} from 'react';
import {selectDateTextStyles} from '../lib/day';
import {dateToISOWithoutTime} from '../../../../../lib/date';

export const DayComponent 
  = memo(function DayComponent(props: DayComponentProps) {
    const styles = createDayStyle(props);

    return (
      <TouchableOpacity
        style={styles.container}
        onPress={() => {
          if (props.onPress) {
            if (props.date) {
              if (props.date?.dateString > dateToISOWithoutTime(props.passedDateUntil)) {
                props.onPress(props.date);
              }
            }
          }
        }}>
        <View
          style={styles.absoluteBackground}/>
        <View style={styles.dateContainer}>
          <Text style={styles[selectDateTextStyles(props)]}>
            {props.date?.day}
          </Text>
        </View>
      </TouchableOpacity>
    );
  });
