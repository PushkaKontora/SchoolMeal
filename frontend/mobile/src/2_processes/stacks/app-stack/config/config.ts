import {ScreenConfig} from '../../../../7_shared/lib/stack-creator';
import {FillerPage} from '../../../../3_pages/filler-page';
import {StackNavigationOptions} from '@react-navigation/stack';
import {AddChildrenPage} from "../../../../3_pages/add-children-page";
import {ChildInformationPage} from "../../../../3_pages/child-information-page/ui/child-information-page";

export const SCREENS: ScreenConfig = {
    'MainChildren': {component: AddChildrenPage},
    'ProfileChild': {component: ChildInformationPage}
};

export const SCREEN_OPTIONS: StackNavigationOptions = {};
