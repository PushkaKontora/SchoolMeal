import {PanelConfig, PanelList, PanelPressListeners} from '../types/types';
import {PanelContent} from '../ui/panel-content';

export function createPanels(config: PanelConfig, listeners: PanelPressListeners): PanelList {
  return {
    canceled: (props) => (
      <PanelContent
        {...config.canceled}
        onButtonPress={listeners.onSubmit}
        {...props}/>
    ),
    submitted: (props) => (
      <PanelContent
        {...config.submitted}
        onButtonPress={listeners.onCancel}
        {...props}/>
    )
  };
}
