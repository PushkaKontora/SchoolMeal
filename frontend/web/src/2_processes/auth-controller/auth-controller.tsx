import {useAppDispatch, useAppSelector} from '../../../store/hooks';
import {useNavigate} from 'react-router-dom';
import {useEffect, useRef} from 'react';
import {useGetCurrentUserQuery} from '../../7_shared/api';
import {checkToken} from './auth-script.ts';
import {chooseRedirectRoute, NO_AUTH_ROUTES} from '../../3_pages/routing';

export function AuthController() {
  const authorized = useAppSelector((state) => state.auth.authorized);
  const {data: currentUser, refetch: refetchUser} = useGetCurrentUserQuery();

  const dispatch = useAppDispatch();
  const navigate = useRef(useNavigate());

  checkToken(dispatch);

  /*
  useEffect(() => {
    (async () => {
      if (authorized === true) {
        await refetchUser();
      } else if (authorized === false) {
        navigate.current(NO_AUTH_ROUTES.login);
      }
    })();
  }, [authorized, refetchUser]);

  useEffect(() => {
    if (currentUser) {
      navigate.current(chooseRedirectRoute(currentUser.role));
    }
  }, [currentUser]);
  */

  return null;
}
