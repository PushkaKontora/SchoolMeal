import {ScreenConfig} from '../../../../7_shared/lib/stack-creator';
import {DebugPage} from '../../../../3_pages/debug-page';
import {StackHeaderProps, StackNavigationOptions} from '@react-navigation/stack';
import {NutritionPage} from '../../../../3_pages/nutrition-page';
import {AddChildrenPage} from '../../../../3_pages/add-children-page';
import {ChildInformationPage} from '../../../../3_pages/child-information-page/ui/child-information-page';
import {AppHeader} from '../../../../4_widgets/app-header';

export const SCREENS: ScreenConfig = {
  'Debug': {
    component: DebugPage
  },
  'MainChildren': {
    component: AddChildrenPage,
    options: {
      header: (props: StackHeaderProps) => (<AppHeader
        {...props}
        showBackButton={false}
        title={'Мои дети'}/>)
    }
  },
  'ProfileChild': {
    component: ChildInformationPage,
    options: {
      header: (props: StackHeaderProps) => (<AppHeader
        {...props}
        showBackButton={true}
        title={'Мой ребенок'}/>)
    }
  },
  'Nutrition': {
    component: NutritionPage,
    options: {
      header: (props: StackHeaderProps) => (<AppHeader
        {...props}
        showBackButton={true}
        title={'Питание'}/>)
    }
  }
};

export const SCREEN_OPTIONS: StackNavigationOptions = {};
