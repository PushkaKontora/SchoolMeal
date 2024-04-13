import {NotificationOut} from '../backend-types/notifications/notifications.ts';
import {Notification} from '../frontend-types/notifications/notifications.ts';

export const toNotification = (notification: NotificationOut): Notification => ({
  id: notification.id,
  body: notification.body,
  read: notification.isRead,
  mark: notification.mark,
  createdAt: new Date(notification.createdAt),
  subtitle: notification.subtitle,
  title: notification.title
});

export const toNotificationArray
  = (notifications: NotificationOut[]): Notification[] => notifications.map(toNotification);
