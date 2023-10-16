import {ChildPersonalInformationProps} from '../model/props';
import {StyleSheet} from 'react-native';

export const createStyle = (props: ChildPersonalInformationProps) => StyleSheet.create({
  container: {
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    paddingVertical: 16,
    paddingHorizontal: 16,
    marginHorizontal: 16,
    marginTop: 18,
  },
});
