import {Text, TouchableOpacity, View} from 'react-native';
import {DayComponentProps} from '../model/props';
import {createDayStyle} from '../const/day-styles';
import {memo} from 'react';
import {selectDateTextStyles} from '../lib/day';
import {TODAY_DATE} from '../config/day-config';
import {dateToISOWithoutTime} from '../../../../../lib/date';

export const DayComponent 
  = memo(function DayComponent(props: DayComponentProps) {
    const styles = createDayStyle(props);

    const today = TODAY_DATE();

    return (
      <TouchableOpacity
        style={styles.container}
        onPress={() => {
          if (props.onPress) {
            if (props.date) {
              if (props.date?.dateString >= dateToISOWithoutTime(today)) {
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
