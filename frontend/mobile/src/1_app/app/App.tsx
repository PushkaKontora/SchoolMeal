import 'react-native-gesture-handler';
import {Provider} from 'react-redux';

import {AppNavigator} from '../../2_processes/app-navigator';
import {store} from '../store/store';
import { MagicModalPortal } from 'react-native-magic-modal';

export function App() {

  return (
    <Provider store={store}>
      <MagicModalPortal />
      <AppNavigator/>
    </Provider>
  );
}
