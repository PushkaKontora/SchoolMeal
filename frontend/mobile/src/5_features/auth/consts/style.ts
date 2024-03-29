import {StyleSheet} from 'react-native';

export const createStyle = () => StyleSheet.create({
  container: {
  },
  titles: {
    flexDirection: 'column',
    gap: 8,
    alignItems: 'center',
    marginBottom: 24
  },
  header: {
    fontWeight: '600',
    fontSize: 28
  },
  subHeader: {
    fontWeight: '400',
    fontSize: 14
  }
});
