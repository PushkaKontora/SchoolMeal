import {RoleSidebarProps} from '../model/props.ts';
import {createActionItems, createItems} from '../lib/create-items.tsx';
import {useNavigate} from 'react-router-dom';
import {AppSidebar} from '../../../../4_widgets/app-sidebar';
import {useState} from 'react';
import {NotificationWindow} from '../../../../7_shared/ui/v2/notifications';
import {Api} from '../../../../7_shared/api';

export function RoleSidebar(props: RoleSidebarProps) {
  const navigate = useNavigate();

  const [isNotificationHidden, setIsNotificationHidden] = useState(true);

  const [readNotifications] = Api.useReadNotificationsMutation();

  const {data: notifications, refetch: refetchNotifications} = Api.useGetNotificationsQuery();

  const [selectedItemIndex, setSelectedItemIndex] = useState(0);
  const items = createItems(setSelectedItemIndex, navigate, props.userRole);
  const actionItems = createActionItems(props.userRole, [
    async () => {
      if (isNotificationHidden) {
        await refetchNotifications();

        const ids = notifications
          ?.filter(n => !n.read)
          ?.map(n => n.id);

        if (ids && ids.length > 0) {
          readNotifications({
            ids: ids
          });
        }
      }
      setIsNotificationHidden(prev => !prev);
    }
  ]);

  return (
    <>
      <AppSidebar
        selectedItemIndex={selectedItemIndex}
        userName={props.userName}
        items={items}
        actionItems={actionItems}
      />
      <NotificationWindow
        notifications={notifications?.map(n => ({
          title: n.title,
          subtitle: n.subtitle,
          className: n.mark,
          body: n.body,
          read: n.read
        })) || []}
        onClose={() => setIsNotificationHidden(true)}
        hidden={isNotificationHidden}/>
    </>
  );
}
