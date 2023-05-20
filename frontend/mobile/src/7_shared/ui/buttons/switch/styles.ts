import {StyleSheet} from 'react-native';

export const createStyle = (toggled: boolean) => StyleSheet.create({
  background: {
    backgroundColor: toggled ? '#2C2C2C' : '#EEEEF0',
    borderRadius: 100,
    paddingVertical: 2.14,
    paddingHorizontal: 2.86,
    width: 37.14,
    alignSelf: 'flex-start',
    alignItems: 'center',
    flexDirection: toggled ? 'row-reverse' : 'row'
  },
  pin: {
    width: 15.71,
    height: 15.71,
    elevation: 3,
    shadowColor: '#000000',
    backgroundColor: '#FFFFFF',
    borderRadius: 100
  }
});
