import {chooseRedirectRoute} from '../../../3_pages/routing';
import {Role} from '../../../7_shared/lib/auth';
import {redirect} from 'react-router-dom';

export function redirectByRole(role: Role) {
  redirect(chooseRedirectRoute(role));
}
