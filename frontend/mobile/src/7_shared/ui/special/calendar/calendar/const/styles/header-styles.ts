import {StyleSheet} from 'react-native';

export const createStyles = () => StyleSheet.create({
  container: {
    width: '100%',
    height: 38,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12
  },
  month: {
    fontWeight: '600',
    fontSize: 14,
    lineHeight: 19.36,
    flex: 1
  },
  iconContainer: {
    width: 20,
    height: 20,
    alignItems: 'center'
  }
});
