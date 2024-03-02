import {ReactElement} from 'react';

export type LogoutButtonProps = {
  icon?: ReactElement,
  accountName: string,
  onClick: () => void
}
