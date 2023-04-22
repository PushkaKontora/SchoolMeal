import {MarginArea} from '../../../7_shared/ui/styling/margin-area';
import {HorizontalLine} from '../../../7_shared/ui/styling/horizontal-line';
import {AuthFeature} from '../../../5_features/auth-feature/ui/auth-feature';
import {HEADER_TITLE, SUBHEADER_TITLE} from '../consts/consts';
import {LoginForm} from '../../../6_entities/user/ui/login-form';
import {LoginPageProps} from '../../../3_pages/login-page/model/props';
import {ButtonSecondary} from '../../../7_shared/ui/buttons/button-secondary/button-secondary';

export function LoginWidget({navigation}: LoginPageProps) {
  const navigateToSignUp = () => {
    navigation.navigate('SignUp');
  };

  return (
    <AuthFeature
      headerTitle={HEADER_TITLE}
      subHeaderTitle={SUBHEADER_TITLE}>

      <MarginArea
        marginBottom={16}>

        <LoginForm/>

      </MarginArea>

      <MarginArea
        marginBottom={16}>
        <HorizontalLine/>
      </MarginArea>

      <ButtonSecondary title={'Зарегистрироваться'} onPress={navigateToSignUp}/>

    </AuthFeature>
  );
}
