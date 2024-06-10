import {NotificationAmountOut, ReadNotificationsBody} from '../../backend-types/notifications/notifications.ts';

export type Notification = {
  id: string,
  read: boolean,
  title: string,
  subtitle: string,
  mark: string,
  body: string,
  createdAt: Date
}

export type ReadNotificationsFrontendParams = ReadNotificationsBody

export type NotificationAmount = NotificationAmountOut
