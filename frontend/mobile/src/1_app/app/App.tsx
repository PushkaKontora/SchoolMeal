import 'react-native-gesture-handler';

import {AuthProvider} from "../../2_processes/contexts/auth-context";
import {AppNavigator} from "../../2_processes/app-navigator";

export function App() {
  console.log(process.env["HMAC_KEY_NAME "]);

  return (
    <AuthProvider>
      <AppNavigator/>
    </AuthProvider>
  );
}
