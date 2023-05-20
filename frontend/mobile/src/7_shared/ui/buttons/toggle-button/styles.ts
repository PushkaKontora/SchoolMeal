import {StyleSheet} from 'react-native';

export const styles = StyleSheet.create({
  background: {
    backgroundColor: '#EEEEF0',
    borderRadius: 100,
    paddingVertical: 3,
    paddingHorizontal: 4,
    gap: 0,
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start'
  },
  active: {
    fontWeight: '500',
    fontSize: 9,
    backgroundColor: '#FFFFFF',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 100,
    textAlign: 'center',
    elevation: 3,
    shadowColor: '#000000'
  },
  activeText: {
    color: '#333333'
  },
  inactive: {
    fontWeight: '500',
    fontSize: 9,
    paddingHorizontal: 12,
    textAlign: 'center'
  },
  inactiveText: {
    color: '#C2C2C4'
  }
});
