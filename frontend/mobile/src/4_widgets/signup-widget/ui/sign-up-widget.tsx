import {SignUpProps} from '../../../3_pages/sign-up-page/model/props';
import {AuthFeature} from '../../../5_features/auth-feature/ui/auth-feature';
import {HEADER_TITLE, SUBHEADER_TITLE} from '../consts/consts';
import {MarginArea} from '../../../7_shared/ui/styling/margin-area';
import {HorizontalLine} from '../../../7_shared/ui/styling/horizontal-line';
import {ButtonSecondary} from '../../../7_shared/ui/buttons/button-secondary/button-secondary';
import {SignUpForm, USER_API} from '../../../6_entities/user';
import {SignUpFormData} from '../../../6_entities/user/ui/sign-up-form/types';
import {AUTH_API, AuthTokenService, TokenResponse} from '../../../5_features/auth';
import {setAuthorized} from '../../../5_features/auth/model/auth-slice/auth-slice';
import {useAppDispatch} from '../../../../store/hooks';

export function SignUpWidget({navigation}: SignUpProps) {
  const navigateToLogin = () => {
    navigation.goBack();
  };

  const [signIn, signInInfo] = AUTH_API.useSignInMutation();
  const [register, registerInfo] = USER_API.useRegisterMutation();

  const dispatch = useAppDispatch();

  const asyncRegister = async (currentData: SignUpFormData) => {
    try {
      const {confirmPassword, ...data} = currentData;
      const loginData = {login: data.phone, password: data.password};

      await register(data);

      const response: {data: TokenResponse} = await signIn(loginData);
      await AuthTokenService.saveAuthToken(response.data);
      dispatch(setAuthorized(true));

      console.log(response.data);
    } catch (error) {
      console.log('Cannot register: ');
      console.log(error);
    }
  };

  const onSubmit = (data: SignUpFormData) => {
    asyncRegister(data);
  };

  const onError = (error: any) => {
    console.log('Register error: ' + JSON.stringify(error));
  };

  return (
    <AuthFeature
      headerTitle={HEADER_TITLE}
      subHeaderTitle={SUBHEADER_TITLE}>

      <MarginArea
        marginBottom={16}>

        <SignUpForm
          onSubmit={onSubmit}
          onError={onError}/>

      </MarginArea>

      <MarginArea
        marginBottom={16}>
        <HorizontalLine/>
      </MarginArea>

      <ButtonSecondary title={'Вход'} onPress={navigateToLogin}/>

    </AuthFeature>
  );
}