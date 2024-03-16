import {PrivateRouteProps} from './props';
import {isRoleMatching} from './utils';
import {useEffect, useState} from 'react';
import {Navigate, useLocation} from 'react-router-dom';
import {useGetCurrentUserQuery} from '../../7_shared/api';
import {useAppSelector} from '../../../store/hooks.ts';

export function PrivateRoute(props: PrivateRouteProps) {
  const authorized = useAppSelector((state) => state.auth.authorized);
  const {data: currentUser, refetch: refetchUser} = useGetCurrentUserQuery();

  const location = useLocation();

  const [roleMatched, setRoleMatched]
    = useState(isRoleMatching(props.requiredRole, currentUser));

  useEffect(() => {
    (async () => {
      if (authorized == true) {
        await refetchUser();
      } else if (authorized == false) {
        setRoleMatched(false);
      } else {
        setRoleMatched(false);
      }
    })();
  }, [authorized, refetchUser]);

  useEffect(() => {
    setRoleMatched(isRoleMatching(props.requiredRole, currentUser));
  }, [props.requiredRole, currentUser]);

  if (roleMatched) {
    return (props.children);
  } else {
    return (<Navigate
      to={props.redirectTo}
      state={{prevLocation: location.pathname}}/>);
  }
}
