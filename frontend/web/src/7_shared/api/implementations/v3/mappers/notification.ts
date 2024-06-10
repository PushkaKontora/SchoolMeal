import {NotificationAmountOut, NotificationOut} from '../backend-types/notifications/notifications.ts';
import {Notification, NotificationAmount} from '../frontend-types/notifications/notifications.ts';

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

export const toNotificationAmount
  = (amount: NotificationAmountOut): NotificationAmount => ({count: amount.count});
