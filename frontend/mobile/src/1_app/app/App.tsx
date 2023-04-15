import 'react-native-gesture-handler';

import {AppNavigator} from '../../2_processes/app-navigator';

export function App() {
  console.log(process.env['HMAC_KEY_NAME ']);

  return (
    <AppNavigator/>
  );
}
