import {PanelConfig, PanelList, PanelPressListeners} from '../types/types';
import {PanelContent} from '../ui/panel-content';

export function createPanels(config: PanelConfig, listeners: PanelPressListeners): PanelList {
  return {
    register: (
      <PanelContent
        {...config.registered}
        onButtonPress={listeners.onRegister}/>
    ),
    deregister: (
      <PanelContent
        {...config.deregistered}
        onButtonPress={listeners.onDeregister}/>
    )
  };
}
