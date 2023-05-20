import {ScreenConfig} from '../../../../7_shared/lib/stack-creator';
import {DebugPage} from '../../../../3_pages/debug-page';
import {StackNavigationOptions} from '@react-navigation/stack';
import {NutritionPage} from '../../../../3_pages/nutrition-page';
import {AddChildrenPage} from '../../../../3_pages/add-children-page';

export const SCREENS: ScreenConfig = {
  'Debug': {
    component: DebugPage
  },
  'MainChildren': {
    component: AddChildrenPage
  },
  'Nutrition': {
    component: NutritionPage
  }
};

export const SCREEN_OPTIONS: StackNavigationOptions = {};
