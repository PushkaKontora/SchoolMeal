import {useAppDispatch, useAppSelector} from '../../../store/hooks';
import {useCurrentUserQuery} from '../../6_entities/user/api/api';
import {useNavigate} from 'react-router-dom';
import {AuthTokenService} from '../../5_features/auth';
import {setAuthorized} from '../../5_features/auth/model/auth-slice/auth-slice';
import {useEffect} from 'react';
import {chooseRedirectRoute} from '../app-navigator/utils';
import {NO_AUTH_ROUTES} from '../../7_shared/config/routes/no-auth-routes';

export function AuthController() {
  const authorized = useAppSelector((state) => state.auth.authorized);
  const {data: currentUser, refetch: refetchUser} = useCurrentUserQuery();

  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const checkToken = () => {
    AuthTokenService.getToken()
      .then(async (value) => {
        const result = value !== null;

        dispatch(setAuthorized(result));
      })
      .catch(() => dispatch(setAuthorized(false)));
  };

  useEffect(() => {
    checkToken();
  }, []);

  useEffect(() => {
    (async () => {
      if (authorized === true) {
        await refetchUser();
      } else if (authorized === false) {
        navigate(NO_AUTH_ROUTES.login);
      }
    })();
  }, [authorized]);

  useEffect(() => {
    if (currentUser) {
      navigate(chooseRedirectRoute(currentUser.role));
    }
  }, [currentUser]);

  return null;
}
