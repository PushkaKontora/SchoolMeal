import {authenticate, setAuthorized} from '../../../7_shared/lib/auth/model/auth-slice';
import {useAppDispatch} from '../../../../store/hooks.ts';
import {NavigateFunction} from 'react-router-dom';
import {chooseRedirectRoute} from '../../../3_pages/routing';
import {AuthTokenProcessor, JwtPayload, Role} from '../../../7_shared/lib/auth';

export function checkRole(
  payload: JwtPayload,
  dispatch: ReturnType<typeof useAppDispatch>,
  navigate: NavigateFunction
) {
  const role: Role = payload.role;
  navigate(chooseRedirectRoute(role));
  dispatch(authenticate({
    jwtPayload: payload,
    userRole: role
  }));
}

// TODO: проверять, истек ли токен
export function takeTokenAndCheckRole(
  dispatch: ReturnType<typeof useAppDispatch>,
  navigate: NavigateFunction
) : Promise<void> {
  const payload = AuthTokenProcessor.getAndDecodeAuthToken();

  if (payload && !AuthTokenProcessor.isTokenExpired(payload)) {
    checkRole(payload, dispatch, navigate);
    return Promise.resolve();
  } else {
    dispatch(setAuthorized(false));
    return Promise.reject();
  }
}

