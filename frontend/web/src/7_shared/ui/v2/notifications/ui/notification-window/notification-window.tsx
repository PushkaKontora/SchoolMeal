import {NotificationWindowProps} from '../../model/props.ts';
import {CloseButton, NotificationWindowContainer, WindowBody} from './styles.ts';
import CloseIcon from '../../assets/close_button.svg?react';
import {NotificationCard} from '../notification-card';

export function NotificationWindow(props: NotificationWindowProps) {
  return (
    <NotificationWindowContainer
      $hidden={props.hidden}>
      <CloseButton
        onClick={props?.onClose}>
        <CloseIcon
          width={'10px'}
          height={'10px'}/>
      </CloseButton>
      <WindowBody>
        {
          props.notifications.map(item => 
            <NotificationCard
              {...item}
            />)
        }
      </WindowBody>
    </NotificationWindowContainer>
  );
}
