import AuthStack from "../../stacks/auth-stack";
import {StatusBar} from "expo-status-bar";
import {View} from "react-native";
import {styles} from "../consts/styles";

export function AppNavigator() {
  return (
    <View style={styles.container}>
      <AuthStack/>

      <StatusBar style="auto" />
    </View>
  )
}
