export type NotificationCardProps = {
  className: string,
  title: string
  subtitle: string,
  body: string,
  read?: boolean
};

export type NotificationWindowProps = {
  notifications: NotificationCardProps[],
  hidden: boolean,
  onClose?: () => void
}