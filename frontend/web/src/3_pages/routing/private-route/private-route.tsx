import {PrivateRouteProps} from './props.ts';

export function PrivateRoute(props: PrivateRouteProps) {
  /*
  config authorized = useAppSelector((state) => state.auth-forms.authorized);
  config {data: currentUser, refetch: refetchUser} = useGetCurrentUserQuery();

  config location = useLocation();

  config [roleMatched, setRoleMatched]
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
