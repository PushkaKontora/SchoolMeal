import {LoginPageProps} from '../model/props';
import {LoginWidget} from '../../../4_widgets/login-widget';

export function LoginPage({navigation}: LoginPageProps) {
  return (
    <LoginWidget
      navigation={navigation}/>
  );
}
