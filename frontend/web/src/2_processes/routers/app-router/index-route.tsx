import {useAppSelector} from '../../../../store/hooks.ts';
import {useEffect} from 'react';
import {useNavigate} from 'react-router-dom';
import {chooseRedirectRoute, NO_AUTH_ROUTES} from '../../../3_pages/routing';

export function IndexRoute() {
  const navigate = useNavigate();

  const authorized = useAppSelector((state) => state['auth'].authorized);
  const jwtPayload = useAppSelector((state) => state['auth'].jwtPayload);

  useEffect(() => {
    if (authorized === false) {
      navigate(NO_AUTH_ROUTES.login);
    } else if (authorized === true && jwtPayload) {
      navigate(chooseRedirectRoute(jwtPayload.role));
    }
  }, [authorized, jwtPayload]);

  return null;
}
