import 'react-native-gesture-handler';
import {Provider} from 'react-redux';

import {AppNavigator} from '../../2_processes/app-navigator';
import {MagicModalPortal} from 'react-native-magic-modal';
import {store} from "../../../store/store";
import {AuthTokenService} from "../../5_features/auth";

export function App() {
    //AuthTokenService.saveAuthToken({accessToken: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwidXNlcl9pZCI6MSwicm9sZSI6InBhcmVudCIsImV4cGlyZXNfaW4iOjE2OTI2MjYzMzB9.sOHBGG9OoHjiP8VLFOfYKKQZ79hODxWfn33q4LtSjMk'})

    return (
        <Provider store={store}>
            <MagicModalPortal/>
            <AppNavigator/>
        </Provider>
    );
}
