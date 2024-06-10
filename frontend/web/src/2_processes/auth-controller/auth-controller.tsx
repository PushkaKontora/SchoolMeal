/**
 * @deprecated
 */
export function AuthController() {
  /*
  const authorized = useAppSelector((state) => state.auth-forms.authorized);
  const {data: currentUser, refetch: refetchUser} = useGetCurrentUserQuery();

  const dispatch = useAppDispatch();
  const navigate = useRef(useNavigate());

  checkToken(dispatch);


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
