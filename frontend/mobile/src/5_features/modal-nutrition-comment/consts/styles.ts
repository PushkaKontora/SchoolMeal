import {StyleSheet} from 'react-native';

export const createStyles = () => StyleSheet.create({
  text: {
    fontWeight: '500',
    fontSize: 14,
    lineHeight: 16.66,
    color: '#121212',
    marginBottom: 16
  },
  buttons: {
    flexDirection: 'row',
    gap: 8
  }
});
