import 'react-native-gesture-handler';
import {Provider} from 'react-redux';

import {AppNavigator} from '../../2_processes/app-navigator';
import {MagicModalPortal} from 'react-native-magic-modal';
import {store} from "../../../store/store";
import {ChildInformationPage} from "../../3_pages/child-information-page/ui/child-information-page";
import {Class} from "../../7_shared/model/class";
import {CancelMealPeriods} from "../../7_shared/model/cancelMealPeriods";
import {Child} from "../../6_entities/child/model/child";

export function App() {
const moks: Child = {
    id: '1',
    lastName: 'Дыков',
    firstName: 'Лима',
    certificateBeforeDate: "2023-05-14T04:49:48.862Z",
    balance: 10000,
    breakfast: true,
    lunch: false,
    dinner: false,
    schoolClass: {
        "id": 1,
        "number": 1,
        "letter": "a",
        "hasBreakfast": true,
        "hasLunch": false,
        "hasDinner": false,
        "teachers": [],
        "school": {
            "id": 1,
            "name": 'УрФУ'
        }
    },
    "cancelMealPeriods": []
}
    return (
        <Provider store={store}>
            <MagicModalPortal/>
            <ChildInformationPage childInformation={moks}/>
            {/*<AppNavigator/>*/}
                </Provider>
                );
            }
