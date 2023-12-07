import {Text, TouchableOpacity, View} from 'react-native';
import {DayComponentProps} from '../model/props';
import {createDayStyle} from '../const/day-styles';
import {memo} from 'react';

export const DayComponent 
  = memo(function DayComponent(props: DayComponentProps) {
    const styles = createDayStyle(props);

    return (
      <TouchableOpacity
        onPress={() => {
          if (props.onPress) {
            props.onPress(props.date);
          }
        }}>
        <View style={styles.container}>
          <View
            style={styles.absoluteBackground}/>
          <View style={styles.dateContainer}>
            <Text style={styles.dateText}>
              {props.date?.day}
            </Text>
          </View>
        </View>
      </TouchableOpacity>

    );
  });
