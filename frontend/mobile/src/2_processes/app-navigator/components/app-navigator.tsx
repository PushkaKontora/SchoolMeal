import AuthStack from '../../stacks/auth-stack';
import {StatusBar} from 'expo-status-bar';
import {View} from 'react-native';
import {styles} from '../consts/styles';
import {NavigationContainer} from '@react-navigation/native';

export function AppNavigator() {
  return (
    <NavigationContainer>
      <View style={styles.container}>
        <AuthStack/>

        <StatusBar style="auto" />

      </View>
    </NavigationContainer>
  );
}

