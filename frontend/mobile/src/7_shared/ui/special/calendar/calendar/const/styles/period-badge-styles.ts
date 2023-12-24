import {StyleSheet} from 'react-native';

export const createPeriodBadgeStyles = () => StyleSheet.create({
  container: {
    alignItems: 'center'
  },
  badge: {
    backgroundColor: '#F7F7F7',
    borderRadius: 6,
    paddingHorizontal: 10,
    paddingVertical: 6,
    gap: 6,
    alignItems: 'center',
    flexDirection: 'row'
  },
  text: {
    color: '#000000',
    fontWeight: '400',
    fontSize: 16,
    verticalAlign: 'middle'
  }
});
