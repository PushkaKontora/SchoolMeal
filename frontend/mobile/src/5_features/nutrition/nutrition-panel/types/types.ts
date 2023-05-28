import {PanelContentProps} from './props';
import {ReactElement} from 'react';

export type PanelNames = 'canceled' | 'submitted';

export type PanelConfig = {
  [index in PanelNames]: Omit<PanelContentProps, 'onButtonPress'>;
};

export type PanelPressListeners = {
  onCancel: () => void,
  onSubmit: () => void
}

export type PanelList = {
  canceled: ReactElement,
  submitted: ReactElement
}
