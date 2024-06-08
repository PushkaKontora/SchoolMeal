import {RoleSidebarProps} from '../model/props.ts';
import {createActionItems, createItems} from '../lib/create-items.tsx';
import {redirect, useNavigate} from 'react-router-dom';
import {AppSidebar} from '../../../../4_widgets/app-sidebar';
import {useState} from 'react';
import {NotificationWindow} from '../../../../7_shared/ui/v2/notifications';
import {Api} from '../../../../7_shared/api';
import {useAppDispatch} from '../../../../../store/hooks.ts';
import {logout} from '../../../../5_features/auth/model/auth-slice';
import {NO_AUTH_ROUTES} from '../../../../3_pages/routing';

export function RoleSidebar(props: RoleSidebarProps) {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const [isNotificationHidden, setIsNotificationHidden] = useState(true);

  /* eslint-disable @typescript-eslint/no-unused-vars */
  // @ts-expect-error Not used for demo
  const [readNotifications] = Api.useReadNotificationsMutation();

  const {data: notifications, refetch: refetchNotifications} = Api.useGetNotificationsQuery();

  const [selectedItemIndex, setSelectedItemIndex] = useState(0);
  const items = createItems(setSelectedItemIndex, navigate, props.userRole);
  const actionItems = createActionItems(props.userRole, [
    async () => {
      if (isNotificationHidden) {
        await refetchNotifications();

        // const ids = notifications
        //   ?.filter(n => !n.read)
        //   ?.map(n => n.id);
        //
        // if (ids && ids.length > 0) {
        //   readNotifications({
        //     ids: ids
        //   });
        // }
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
        onLogoutClick={() => {
          dispatch(logout());
          redirect(NO_AUTH_ROUTES.login);
        }}
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
