import {StyleSheet} from 'react-native';
import {DayComponentProps} from '../../model/props';
import {isBorderDay, selectAbsoluteBackgroundStyles} from '../../lib/lib';

export const createDayStyle = (props: DayComponentProps) => StyleSheet.create({
  container: {
    width: '100%',
    height: 36,
    alignItems: 'center'
  },
  absoluteBackground: {
    position: 'absolute',
    height: 36,
    ...selectAbsoluteBackgroundStyles(props)
  },
  dateContainer: {
    width: 36,
    height: 36,
    borderRadius: 50,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: isBorderDay(props) ? '#E9632C' : '#00000000'
  },
  dateText: {
    fontSize: 17.6,
    fontWeight: isBorderDay(props) ? '600' : '400',
    color: isBorderDay(props) ? '#FFFFFF' : '#000000'
  },
  pastDateText: {
    fontSize: 17.6,
    fontWeight: '400',
    color: '#C4C4C7'
  }
});
