import {ScreenConfig} from "./types";
import {createStackNavigator} from "@react-navigation/stack";

export function generateStack(config: ScreenConfig) {
  const STACK = createStackNavigator();

  return (
    <STACK.Navigator>
      {
        Object.keys(config)
          .map((key) =>
            <STACK.Screen name={key} {...config[key]}/>)
      }
    </STACK.Navigator>
  )
}
