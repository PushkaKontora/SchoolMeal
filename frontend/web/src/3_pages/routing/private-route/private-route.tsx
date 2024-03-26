import {PrivateRouteProps} from './props.ts';
import {isRoleMatching} from './utils.ts';
import {useEffect, useState} from 'react';
import {Navigate, useLocation} from 'react-router-dom';
import {useAppSelector} from '../../../../store/hooks.ts';
import {useGetCurrentUserQuery} from '../../../7_shared/api/deprecated/api.ts';

export function PrivateRoute(props: PrivateRouteProps) {
  /*
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
  */

  return (props.children);
}
