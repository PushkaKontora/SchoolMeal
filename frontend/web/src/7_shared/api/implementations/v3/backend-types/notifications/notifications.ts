export type NotificationOut = {
  id: string,
  isRead: boolean,
  title: string,
  subtitle: string,
  mark: string,
  body: string,
  createdAt: string
}

export type NotificationListOut = NotificationOut[]

export type ReadNotificationsBody = {
  ids: NotificationOut['id'][]
}

export type NotificationAmountOut = {
  count: number
}
