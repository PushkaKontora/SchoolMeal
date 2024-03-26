import { BrowserRouter } from 'react-router-dom';
import { AppRouter } from '../../../routers/app-router';
import { useAppSelector } from '../../../../../store/hooks.ts';
import { AuthController } from '../../../auth-controller';
import {RoleSidebar} from '../../../role-sidebar/role-sidebar/ui/role-sidebar.tsx';
import {SidebarAndContent} from '../../../role-sidebar/sidebar-and-content';
import {useGetCurrentUserQuery} from '../../../../7_shared/api/deprecated/api.ts';

/**
 * @deprecated Излишняя абстракция, все тело компонента теперь в App
 */
export function AppNavigator() {
  const authorized = useAppSelector((state) => state.auth.authorized);

  const {data: currentUser} = useGetCurrentUserQuery();

  return (
    <BrowserRouter>
      <AuthController/>
      <SidebarAndContent
        shouldShowSidebar={authorized}
        sidebar={(
          <RoleSidebar
            currentUser={currentUser}/>
        )}
        contentStyles={{
          padding: '48px 40px 0 40px'
        }}>
        {/*<AppRouter/>*/}
      </SidebarAndContent>
    </BrowserRouter>
  );
}
