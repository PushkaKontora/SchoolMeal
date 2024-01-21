import {MarginArea} from '../../../7_shared/ui/styling/margin-area';
import {HorizontalLine} from '../../../7_shared/ui/styling/horizontal-line';
import {AuthFeature} from '../../../5_features/auth';
import {HEADER_TITLE, SUBHEADER_TITLE} from '../consts/strings';
import {LoginForm, LoginFormData} from '../../../6_entities/user';
import {LoginPageProps} from '../../../3_pages/login-page/model/props';
import {ButtonSecondary} from '../../../7_shared/ui/buttons/button-secondary/button-secondary';
import {AUTH_API, TokenResponse} from '../../../5_features/auth';
import {AuthTokenService} from '../../../5_features/auth';
import {setAuthorized} from '../../../5_features/auth/model/auth-slice/auth-slice';
import {useAppDispatch} from '../../../../store/hooks';
import {TokenPayload} from '../../../5_features/auth/model/token-payload';
import {useEffect, useState} from 'react';
import {ToastService} from '../../../7_shared/lib/toast-service';
import {ERROR_MESSAGES_TITLES} from '../config/errors';

export function LoginWidget({navigation}: LoginPageProps) {
  const navigateToSignUp = () => {
    navigation.navigate('SignUp');
  };

  const [signIn, {data, isSuccess, isError, error}] =
    AUTH_API.useSignInMutation();
  const dispatch = useAppDispatch();

  const [formDisabled, setFormDisabled] = useState(false);

  const saveToken = async (data: TokenPayload) => {
    await AuthTokenService.saveAuthToken(data);
    dispatch(setAuthorized(true));
  };

  const onSubmit = async (currentData: LoginFormData) => {
    setFormDisabled(true);
    await signIn(currentData);
  };

  useEffect(() => {
    if (isSuccess) {
      saveToken(data as TokenResponse);
    }
  }, [isSuccess]);

  useEffect(() => {
    if (isError) {
      setFormDisabled(false);

      const typedError = error as {
        status: number,
        data: {
          detail: string
        }
      };
      ToastService.show('danger', {
        title: ERROR_MESSAGES_TITLES[typedError.status] || ERROR_MESSAGES_TITLES.other,
        description: typedError.data.detail
      });
    }
  }, [isError]);

  return (
    <AuthFeature
      headerTitle={HEADER_TITLE}
      subHeaderTitle={SUBHEADER_TITLE}>

      <MarginArea
        marginBottom={16}>

        <LoginForm
          onSubmit={onSubmit}
          disabled={formDisabled}/>

      </MarginArea>

      <MarginArea
        marginBottom={16}>
        <HorizontalLine/>
      </MarginArea>

      <ButtonSecondary title={'Зарегистрироваться'} onPress={navigateToSignUp}/>

    </AuthFeature>
  );
}
