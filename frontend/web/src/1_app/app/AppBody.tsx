import {useAppDispatch, useAppSelector} from '../../../store/hooks.ts';
import {RoleController, takeTokenAndCheckRole} from '../../2_processes/role-controller';
import {SidebarAndContent} from '../../2_processes/role-sidebar/sidebar-and-content';
import {RoleSidebar} from '../../2_processes/role-sidebar/role-sidebar/ui/role-sidebar.tsx';
import {getFullName} from '../../6_entities/user';
import {AppRouter} from '../../2_processes/routers/app-router';
import {AuthTokenProcessor} from '../../5_features/auth';

import 'react-toastify/dist/ReactToastify.css';
import {AppToastContainer} from '../../7_shared/ui/v2/toast';
import {useNavigate} from 'react-router-dom';

export function AppBody() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const authorized = useAppSelector((state) => state['auth'].authorized);
  const jwtPayload = useAppSelector((state) => state['auth'].jwtPayload);
  //
  // useEffect(() => {
  //   if (authorized === true && jwtPayload) {
  //     redirect(chooseRedirectRoute(jwtPayload.role));
  //     console.log('Aaaa');
  //   }
  // }, [authorized, jwtPayload]);

  return (
    <>
      <AppToastContainer/>
      <RoleController/>
      <SidebarAndContent
        shouldShowSidebar={authorized}
        sidebar={(
          <RoleSidebar
            userRole={jwtPayload?.role}
            userName={getFullName({
              firstName: jwtPayload?.first_name,
              lastName: jwtPayload?.last_name
            })}/>
        )}
        contentStyles={{
          padding: '40px'
        }}>
        <AppRouter
          loginPageProps={{
            onSuccess: (response) => {
              AuthTokenProcessor.saveAuthToken(response.token);
              return takeTokenAndCheckRole(dispatch, navigate);
            }
          }}/>
      </SidebarAndContent>
    </>
  );
}
