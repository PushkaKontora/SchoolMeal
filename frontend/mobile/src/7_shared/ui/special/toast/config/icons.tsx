import NotificationPositiveIcon from '../../../../assets/images/notification-positive.svg';
import NotificationNegativeIcon from '../../../../assets/images/notification-negative.svg';
import React from 'react';

export const ICON_SIZE = 40;

export const ICONS: {[index: string]: React.JSX.Element} = {
  success: <NotificationPositiveIcon
    width={ICON_SIZE}
    height={ICON_SIZE}/>,
  danger: <NotificationNegativeIcon
    width={ICON_SIZE}
    height={ICON_SIZE}/>
};

