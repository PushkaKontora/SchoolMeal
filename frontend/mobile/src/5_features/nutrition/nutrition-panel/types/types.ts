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

export type PanelListItem =
  (props: Partial<PanelContentProps>) => ReactElement;

export type PanelList = {
  canceled: PanelListItem,
  submitted: PanelListItem
}
