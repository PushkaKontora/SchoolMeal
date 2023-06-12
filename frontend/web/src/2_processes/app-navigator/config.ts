import {EMPLOYEE_ROUTES} from '../../7_shared/config/routes/auth-routes';
import {Role} from '../../7_shared/model/role';

export const ROLE_DEFAULT_ROUTES: {[index: string]: string} = {
  [Role.employee]: EMPLOYEE_ROUTES.application
}
