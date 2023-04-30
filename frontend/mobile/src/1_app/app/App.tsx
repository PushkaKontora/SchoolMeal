import 'react-native-gesture-handler';

import {AppNavigator} from '../../2_processes/app-navigator';
import { MagicModalPortal } from 'react-native-magic-modal';

export function App() {
  console.log(process.env['HMAC_KEY_NAME ']);

  return (
      <>
        <MagicModalPortal />
        <AppNavigator/>
      </>
  );
}
