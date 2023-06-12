import {PrivateRouteProps} from './props';
import {useCurrentUserQuery} from '../../6_entities/user/api/api';
import {isRoleMatching} from './utils';
import {useEffect, useState} from 'react';
import {Navigate, useLocation} from 'react-router-dom';
import {DEFAULT_REDIRECT} from './config';

export function PrivateRoute(props: PrivateRouteProps) {
  const {data: currentUser, refetch: refetchCurrentUser} = useCurrentUserQuery();

  const location = useLocation();

  const [roleMatched, setRoleMatched] = useState(isRoleMatching(props.requiredRole, currentUser));

  useEffect(() => {
    setRoleMatched(isRoleMatching(props.requiredRole, currentUser));
  }, [currentUser]);

  if (roleMatched) {
    return (props.children);
  } else {
    return (<Navigate
      to={props.redirectTo || DEFAULT_REDIRECT}
      state={{prevLocation: location.pathname}}/>);
  }
}
