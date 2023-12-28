import {CalendarHeaderProps} from '../model/props';
import {Text, TouchableOpacity, View} from 'react-native';
import {createStyles} from '../const/styles/header-styles';
import ChevronOrangeLeft from '../../../../../assets/images/chevron-orange-left.svg';
import ChevronOrangeRight from '../../../../../assets/images/chevron-orange-right.svg';
import {dateToHeaderString} from '../lib/header';

export function CalendarHeader(props: CalendarHeaderProps) {
  const styles = createStyles();

  return (
    <View
      style={styles.container}>
      <Text
        style={styles.month}>
        {dateToHeaderString(props.monthDate)}
      </Text>
      <TouchableOpacity
        onPress={props.onLeftPress}>
        <ChevronOrangeLeft
          width={24}
          height={24}/>
      </TouchableOpacity>
      <TouchableOpacity
        onPress={props.onRightPress}>
        <ChevronOrangeRight
          width={24}
          height={24}/>
      </TouchableOpacity>
    </View>
  );
}