import {Button, Text, View} from 'react-native';
import {SignUpProps} from '../model/props';

export function SignUpPage({navigation}: SignUpProps) {
  const loginButtonHandler = () => {
    navigation.goBack();
  };

  return (
    <View>
      <Text>Sign up page</Text>

      <Button title={'Войти'} onPress={loginButtonHandler}/>
    </View>
  );
}
