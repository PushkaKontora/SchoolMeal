/* eslint-disable no-console */

import {ScrollView, Text, View} from 'react-native';
import {ButtonPrimary} from '../../../7_shared/ui/buttons/button-primary';
import {AUTH_API, AuthTokenService} from '../../../5_features/auth';
import {useAppDispatch} from '../../../../store/hooks';
import {setAuthorized} from '../../../5_features/auth/model/auth-slice/auth-slice';
import {PropsWithNavigation} from '../../../7_shared/model/props-with-navigation';
import {USER_API} from '../../../6_entities/user';
import {useGetChildrenQuery} from '../../../6_entities/child/api/api';
import {useEffect} from 'react';
import {magicModal} from 'react-native-magic-modal';
import {ModalMealPeriod} from '../../../5_features/modal-meal-period';

export function DebugPage({navigation}: PropsWithNavigation) {
  const {data: currentUser, refetch: refetchUser} = USER_API.useCurrentUserQuery();
  const {data: children, refetch: refetchChildren} = useGetChildrenQuery();
  const [refreshToken] = AUTH_API.useRefreshTokensMutation();
  const dispatch = useAppDispatch();

  useEffect(() => {
    const doAsyncEffect = async () => {
      await refetchUser();
      await refetchChildren();
    };
    doAsyncEffect();
  }, []);

  const logout = async () => {
    await AuthTokenService.deleteToken();
    dispatch(setAuthorized(false));
  };

  const showToken = async () => {
    const token = await AuthTokenService.getToken();
    console.log('Current token: ');
    console.log(token);
  };

  const handleTokenRefresh = async () => {
    const tokenResponse = await refreshToken().unwrap();
    await AuthTokenService.saveAuthToken(tokenResponse);
    await showToken();
  };

  const getUserData = async () => {
    console.log(currentUser);
  };

  const toMain = () => {
    navigation.navigate('MainChildren');
  };

  const toNutrition = () => {
    if (children && children[0]) {
      const child = children[0];
      navigation.navigate('Nutrition', {
        childId: child.id
      });
    } else {
      console.log(children);
    }
  };

  const showCalendar = () => {
    magicModal.show(() => <ModalMealPeriod/>);
  };

  return (
    <ScrollView>
      <View style={{display: 'flex', rowGap: 16, padding: 16}}>
        <Text>Пользователь</Text>
        <ButtonPrimary title={'Выйти из аккаунта'} onPress={logout}/>
        <ButtonPrimary title={'Токен в консоль'} onPress={showToken}/>
        <ButtonPrimary title={'Вызвать refresh-tokens'} onPress={handleTokenRefresh}/>
        <ButtonPrimary title={'Данные пользователя в консоль'} onPress={getUserData}/>
        <Text>Экраны</Text>
        <ButtonPrimary title={'На главную'} onPress={toMain}/>
        <ButtonPrimary title={'Питание'} onPress={toNutrition}/>
        <Text>Модальные окна</Text>
        <ButtonPrimary title={'Снять с питания (Календарь)'} onPress={showCalendar}/>
      </View>
    </ScrollView>
  );
}
