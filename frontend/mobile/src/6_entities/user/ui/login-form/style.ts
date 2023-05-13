import {StyleSheet} from 'react-native';
import {LoginFormProps} from './props';

export const createStyle = (props: LoginFormProps) => StyleSheet.create({
  container: {

  },
  form: {
    flexDirection: 'column',
    gap: 12,
    marginBottom: 16
  }
});
