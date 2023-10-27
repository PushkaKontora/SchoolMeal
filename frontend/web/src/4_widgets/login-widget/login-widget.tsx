import {Content} from '../../7_shared/ui/markup/content';
import {LoginForm} from '../../5_features/auth/ui/login-form';
import {AuthTokenService, TokenResponse, useSignInMutation} from '../../5_features/auth';
import {LoginFormData} from '../../5_features/auth/ui/login-form/types';
import {setAuthorized} from '../../5_features/auth/model/auth-slice/auth-slice';
import {useAppDispatch} from '../../../store/hooks';

export function LoginWidget() {
  const [signIn] = useSignInMutation();
  const dispatch = useAppDispatch();

  const onSubmit = async (data: LoginFormData) => {
    const response: {data: TokenResponse} = await signIn(data);
    await AuthTokenService.saveAuthToken(response.data);
    dispatch(setAuthorized(true));
  };

  return (
    <Content>
      <LoginForm
        onSubmit={onSubmit}/>
    </Content>
  );
}
