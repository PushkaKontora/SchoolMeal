import {PropsWithChildren} from 'react';
import {RoleOrAny} from './types';

export type PrivateRouteProps = {
  requiredRole: RoleOrAny,
  redirectTo?: string
} & PropsWithChildren;
