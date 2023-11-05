import {StyleSheet} from 'react-native';

export const createStyle = () => StyleSheet.create({
  container: {
    alignItems: 'center',
    gap: 4
  },
  icon: {
    width: 92,
    height: 92
  },
  successText: {
    fontWeight: '500',
    fontSize: 16,
    textAlign: 'center',
    color: '#B1B1B1'
  }
});
