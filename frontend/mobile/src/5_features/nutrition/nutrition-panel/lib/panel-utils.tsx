import {PanelConfig, PanelList, PanelPressListeners} from '../types/types';
import {PanelContent} from '../ui/panel-content';

export function createPanels(config: PanelConfig, listeners: PanelPressListeners): PanelList {
  return {
    canceled: (
      <PanelContent
        {...config.canceled}
        onButtonPress={listeners.onSubmit}/>
    ),
    submitted: (
      <PanelContent
        {...config.submitted}
        onButtonPress={listeners.onCancel}/>
    )
  };
}
