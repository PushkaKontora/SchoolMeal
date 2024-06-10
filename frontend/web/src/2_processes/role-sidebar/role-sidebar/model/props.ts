import {Role} from '../../../../7_shared/lib/auth';
import {
  NotificationAmount
} from '../../../../7_shared/api/implementations/v3/frontend-types/notifications/notifications.ts';

export type RoleSidebarProps = {
  userRole?: Role,
  userName?: string
};

export type NotificationBadgeProps = {
  value?: NotificationAmount
}
