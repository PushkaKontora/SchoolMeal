import {LoginPage} from '../../../../3_pages/login-page';
import {ScreenConfig} from '../../../../7_shared/lib/stack-creator';
import {SignUpPage} from '../../../../3_pages/sign-up-page/ui/sign-up-page';
import {StackNavigationOptions} from '@react-navigation/stack';
import {Header} from '../ui/header';

export const SCREENS: ScreenConfig = {
  'Login': {
    component: LoginPage
  },
  'SignUp': {
    component: SignUpPage
  }
};

export const SCREEN_OPTIONS: StackNavigationOptions = {
  header: ({navigation}) => <Header navigation={navigation}/>,
  cardStyle: {
    backgroundColor: '#FFFFFF'
  }
};
