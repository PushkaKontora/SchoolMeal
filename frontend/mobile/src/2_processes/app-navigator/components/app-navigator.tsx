import {StatusBar} from 'expo-status-bar';
import {View} from 'react-native';
import {styles} from '../consts/styles';
import {NavigationContainer} from '@react-navigation/native';
import {useEffect} from 'react';
import {AuthTokenService} from '../../../5_features/auth';
import {useAppDispatch, useAppSelector} from '../../../../store/hooks';
import {setAuthorized} from '../../../5_features/auth/model/auth-slice/auth-slice';
import {LoadingWidget} from '../../../4_widgets/loading-widget/ui/loading-widget';
import AppStack from '../../stacks/app-stack';
import AuthStack from '../../stacks/auth-stack';

export function AppNavigator() {
  const authorized = useAppSelector((state) => state.auth.authorized);
  const dispatch = useAppDispatch();

  const checkToken = () => {
    AuthTokenService.getToken()
      .then((value) => {
        const result = value !== null;

        dispatch(setAuthorized(result));
      })
      .catch(() => dispatch(setAuthorized(false)));
  };

  useEffect(() => {
    checkToken();
  }, []);

  return (
    <View style={styles.container}>
      <NavigationContainer>
        {
          (authorized === undefined) && (
            <LoadingWidget/>
          )
        }
        {
          (authorized === false) && (
            <AuthStack/>
          )
        }
        {
          (authorized === true) && (
            <AppStack/>
          )
        }
        <StatusBar style="auto" />
      </NavigationContainer>
    </View>
  );
}

