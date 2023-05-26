import {PanelContentProps} from './props';
import {ReactElement} from 'react';

export type PanelConfig = {[index: string]: Omit<PanelContentProps, 'onButtonPress'>}

export type PanelPressListeners = {
  onRegister: () => void,
  onDeregister: () => void
}

export type PanelList = {
  register: ReactElement,
  deregister: ReactElement
}
