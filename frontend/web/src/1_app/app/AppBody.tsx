import {useAppDispatch, useAppSelector} from '../../../store/hooks.ts';
import {RoleController, takeTokenAndCheckRole} from '../../2_processes/role-controller';
import {SidebarAndContent} from '../../2_processes/role-sidebar/sidebar-and-content';
import {RoleSidebar} from '../../2_processes/role-sidebar/role-sidebar/ui/role-sidebar.tsx';
import {getFullName} from '../../6_entities/user';
import {AppRouter} from '../../2_processes/routers/app-router';
import {AuthTokenService} from '../../5_features/auth';

export function AppBody() {
  const dispatch = useAppDispatch();

  const authorized = useAppSelector((state) => state['auth'].authorized);
  const jwtPayload = useAppSelector((state) => state['auth'].jwtPayload);

  return (
    <>
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
          padding: '48px 40px 0 40px'
        }}>
        <AppRouter
          loginPageProps={{
            onSuccess: (response) => {
              AuthTokenService.saveAuthToken(response.token);
              return takeTokenAndCheckRole(dispatch);
            }
          }}/>
      </SidebarAndContent>
    </>
  );
}
