import {ScreenConfig} from './types';
import {createStackNavigator, StackNavigationOptions} from '@react-navigation/stack';

export function generateStack(config: ScreenConfig, screenOptions?: StackNavigationOptions) {
  const STACK = createStackNavigator();

  return (
    <STACK.Navigator screenOptions={screenOptions}>
      {
        Object.keys(config)
          .map((key) =>
            <STACK.Screen key={key} name={key} {...config[key]}/>)
      }
    </STACK.Navigator>
  );
}
