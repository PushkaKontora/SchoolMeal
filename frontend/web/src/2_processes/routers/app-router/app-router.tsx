import {Route, Routes} from 'react-router-dom';
import {NO_AUTH_ROUTES} from '../../../7_shared/config/routes/no-auth-routes';
import {LoginPage} from '../../../3_pages/login-page';
import {CANTEEN_STAFF_ROUTES, TEACHER_ROUTES} from '../../../7_shared/config/routes/auth-routes';
import {PrivateRoute} from '../../../5_features/private-route';
import {Role} from '../../../7_shared/model/role';
import {MealApplicationPage} from '../../../3_pages/meal-application-page';
import {Sidebar} from '../../../7_shared/ui/v2/sidebar';
import {useGetCurrentUserQuery} from '../../../7_shared/api';
import {getAccountName} from '../../role-sidebar/lib/account-name.ts';

export function AppRouter() {
  const {data: currentUser}
    = useGetCurrentUserQuery();

  return (
    <Routes>
      <Route
        path={NO_AUTH_ROUTES.login}
        element={<LoginPage/>}/>

      <Route
        path={CANTEEN_STAFF_ROUTES.applications}
        element={
          <PrivateRoute
            requiredRole={Role.canteen_staff}>
            {null}
          </PrivateRoute>
        }/>
      <Route
        path={TEACHER_ROUTES.apply}
        element={
          <PrivateRoute
            requiredRole={Role.teacher}>
            <MealApplicationPage
              sidebar={
                <Sidebar
                  selectedItemIndex={1}
                  items={[
                    {
                      text: 'Мои классы',
                      onClick: () => {return;}
                    },
                    {
                      text: 'Подать заявку',
                      onClick: () => {return;},
                      active: true
                    },
                    {
                      text: 'История заявок',
                      onClick: () => {return;}
                    }
                  ]}
                  actionItems={[
                    {
                      text: 'Уведомления',
                      onClick: () => {return;}
                    }
                  ]}
                  logoutButtonProps={{
                    accountName: getAccountName(currentUser),
                    onClick: () => {return;}
                  }}/>
              }/>
          </PrivateRoute>
        }/>
    </Routes>
  );
}
