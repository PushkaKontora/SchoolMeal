import {StyleSheet} from 'react-native';
import {LoginPageProps} from '../../../../3_pages/login-page/model/props';

export const createStyle = (props: LoginPageProps) => StyleSheet.create({
  container: {

  },
  form: {
    flexDirection: 'column',
    gap: 12,
    marginBottom: 16
  }
});
