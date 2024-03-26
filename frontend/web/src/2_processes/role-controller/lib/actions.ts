import {AuthTokenService, JwtPayload, Role} from '../../../5_features/auth';
import {redirectByRole} from './redirect-by-role.ts';
import {authenticate} from '../../../5_features/auth/model/auth-slice';
import {useAppDispatch} from '../../../../store/hooks.ts';

export function checkRole(
  payload: JwtPayload,
  dispatch: ReturnType<typeof useAppDispatch>) {
  const role: Role = payload.role;
  redirectByRole(role);
  dispatch(authenticate({
    jwtPayload: payload,
    userRole: role
  }));
}

// TODO: проверять, истек ли токен
export function takeTokenAndCheckRole(
  dispatch: ReturnType<typeof useAppDispatch>
) : Promise<void> {
  const payload = AuthTokenService.getAndDecodeAuthToken();

  if (payload && !AuthTokenService.isTokenExpired(payload)) {
    checkRole(payload, dispatch);
    return Promise.resolve();
  } else {
    return Promise.reject();
  }
}

