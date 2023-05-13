import 'react-native-gesture-handler';
import {Provider} from 'react-redux';

import {AppNavigator} from '../../2_processes/app-navigator';
import {store} from '../../../store/store';

export function App() {
  
  return (
    <Provider store={store}>
      <AppNavigator/>
    </Provider>
  );
}
