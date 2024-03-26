import {useAppDispatch} from '../../../store/hooks.ts';
import {takeTokenAndCheckRole} from './lib/actions.ts';
import {Api} from '../../7_shared/api';
import {AuthTokenService} from '../../5_features/auth';
import {NO_AUTH_ROUTES} from '../../3_pages/routing';
import {useNavigate} from 'react-router-dom';
import {useEffect} from 'react';

export function RoleController() {
  const navigate = useNavigate();
  
  const dispatch = useAppDispatch();

  const [refreshToken] = Api.useRefreshMutation();

  useEffect(() => {
    takeTokenAndCheckRole(dispatch)
      .catch(() =>
        refreshToken({
          fingerprint: 'aaaaa'
        }).unwrap()
      )
      .then(response => {
        if (response) {
          AuthTokenService.saveAuthToken(response.token);
          return takeTokenAndCheckRole(dispatch);
        }
      })
      .catch(() => {
        navigate(NO_AUTH_ROUTES.login);
      });
  }, [dispatch, navigate, refreshToken]);

  return null;
}
