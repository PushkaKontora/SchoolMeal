import {MarginArea} from '../../../7_shared/ui/styling/margin-area';
import {HorizontalLine} from '../../../7_shared/ui/styling/horizontal-line';
import {AuthFeature} from '../../../5_features/auth-feature/ui/auth-feature';
import {HEADER_TITLE, SUBHEADER_TITLE} from '../consts/consts';
import {LoginForm, LoginFormData} from '../../../6_entities/user';
import {LoginPageProps} from '../../../3_pages/login-page/model/props';
import {ButtonSecondary} from '../../../7_shared/ui/buttons/button-secondary/button-secondary';
import {AUTH_API, TokenResponse} from '../../../5_features/auth';
import {AuthTokenService} from '../../../5_features/auth';
import {setAuthorized} from '../../../5_features/auth/model/auth-slice/auth-slice';
import {useAppDispatch} from '../../../../store/hooks';

export function LoginWidget({navigation}: LoginPageProps) {
  const navigateToSignUp = () => {
    navigation.navigate('SignUp');
  };

  const [signIn, {error}] = AUTH_API.useSignInMutation();
  const dispatch = useAppDispatch();

  const saveToken = async (currentData: LoginFormData) => {
    const response: {data: TokenResponse} = await signIn(currentData);
    await AuthTokenService.saveAuthToken(response.data);
    dispatch(setAuthorized(true));

    console.log(response.data);
  };

  const onSubmit = (currentData: LoginFormData) => {
    saveToken(currentData);
  };

  const onError = (error: any) => {
    console.log('Error:');
    console.log(error);
  };

  return (
    <AuthFeature
      headerTitle={HEADER_TITLE}
      subHeaderTitle={SUBHEADER_TITLE}>

      <MarginArea
        marginBottom={16}>

        <LoginForm
          onSubmit={onSubmit}
          onError={onError}/>

      </MarginArea>

      <MarginArea
        marginBottom={16}>
        <HorizontalLine/>
      </MarginArea>

      <ButtonSecondary title={'Зарегистрироваться'} onPress={navigateToSignUp}/>

    </AuthFeature>
  );
}
