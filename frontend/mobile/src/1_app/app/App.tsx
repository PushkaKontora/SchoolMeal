import 'react-native-gesture-handler';
import {Provider} from 'react-redux';

import {AppNavigator} from '../../2_processes/app-navigator';
import {MagicModalPortal} from 'react-native-magic-modal';
import {store} from '../../../store/store';
import {ToastNotifier} from '../../4_widgets/toast-notifier';

export function App() {
  return (
    <ToastNotifier>
      <Provider store={store}>
        <MagicModalPortal/>
        <AppNavigator/>
      </Provider>
    </ToastNotifier>
  );
}
