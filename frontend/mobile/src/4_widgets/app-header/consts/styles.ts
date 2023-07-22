import {StyleSheet} from 'react-native';
import {HEIGHT, MARGIN_TOP} from '../config/config';

export const styles = StyleSheet.create({
  container: {
    width: '100%',
    height: HEIGHT + MARGIN_TOP,
    backgroundColor: '#2C2C2C'
  },
  body: {
    width: '100%',
    marginTop: MARGIN_TOP,
    height: HEIGHT,
    justifyContent: 'center',
    alignItems: 'center'
  },
  title: {
    fontSize: 20,
    fontWeight: '600',
    color: '#F6F6F6'
  },
  back: {
    position: 'absolute',
    left: 16
  },
  children: {
    position: 'absolute',
    right: 16
  }
});
