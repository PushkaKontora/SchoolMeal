import {AuthFeatureProps} from '../model/props';
import {StyleSheet} from 'react-native';

export const createStyle = (props: AuthFeatureProps) => StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column'
  },
  titles: {
    flexDirection: 'column',
    gap: 8,
    justifyContent: 'center',
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
