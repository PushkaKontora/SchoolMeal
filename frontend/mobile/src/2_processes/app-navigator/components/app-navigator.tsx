import AuthStack from '../../stacks/auth-stack';
import {StatusBar} from 'expo-status-bar';
import {View} from 'react-native';
import {styles} from '../consts/styles';
import {NavigationContainer} from '@react-navigation/native';

export function AppNavigator() {
  return (
    <View style={styles.container}>
      <NavigationContainer>
        <AuthStack/>

        <StatusBar style="auto" />
      </NavigationContainer>
    </View>
  );
}

