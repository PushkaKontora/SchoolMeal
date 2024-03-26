import {chooseRedirectRoute} from '../../../3_pages/routing';
import {Role} from '../../../5_features/auth';
import {redirect} from 'react-router-dom';

export function redirectByRole(role: Role) {
  redirect(chooseRedirectRoute(role));
}
