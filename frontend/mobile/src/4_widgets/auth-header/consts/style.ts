import {StyleSheet} from 'react-native';
import Constants from 'expo-constants';

export const STYLES = StyleSheet.create({
  container: {
    padding: 8,
    paddingTop: Constants.statusBarHeight + 8,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center'
  },

  headerText: {
    fontWeight: '600',
    fontSize: 19
  }
});
