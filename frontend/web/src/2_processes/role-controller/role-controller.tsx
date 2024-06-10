import {useAppDispatch} from '../../../store/hooks.ts';
import {takeTokenAndCheckRole} from './lib/actions.ts';
import {Api} from '../../7_shared/api';
import {NO_AUTH_ROUTES} from '../../3_pages/routing';
import {useNavigate} from 'react-router-dom';
import {useEffect} from 'react';
import {AuthTokenProcessor} from '../../7_shared/lib/auth';

export function RoleController() {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const [refreshToken] = Api.useRefreshMutation();

  useEffect(() => {
    takeTokenAndCheckRole(dispatch, navigate)
      .catch(() =>
        refreshToken({
          fingerprint: 'aaaaa'
        }).unwrap()
      )
      .then(response => {
        if (response) {
          AuthTokenProcessor.saveAuthToken(response.token);
          return takeTokenAndCheckRole(dispatch, navigate);
        }
      })
      .catch(() => {
        navigate(NO_AUTH_ROUTES.login);
      });
    /* eslint-disable react-hooks/exhaustive-deps */
  }, []);

  return null;
}
