import 'react-native-gesture-handler';

import {AppNavigator} from '../../2_processes/app-navigator';
import {AddChildrenPage} from '../../3_pages/add-children-page/ui/add-children-page';
import { MagicModalPortal } from 'react-native-magic-modal';

export function App() {
  console.log(process.env['HMAC_KEY_NAME ']);

  return (
      <>
        <MagicModalPortal />
        <AddChildrenPage/>
        {/*<AppNavigator/>*/}
      </>
  );
}
