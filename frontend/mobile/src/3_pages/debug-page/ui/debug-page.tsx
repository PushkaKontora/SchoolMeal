import {Text, View} from 'react-native';
import {ButtonPrimary} from '../../../7_shared/ui/buttons/button-primary';
import {AuthTokenService} from '../../../5_features/auth';
import {useAppDispatch} from '../../../../store/hooks';
import {setAuthorized} from '../../../5_features/auth/model/auth-slice/auth-slice';
import {PropsWithNavigation} from '../../../7_shared/model/props-with-navigation';

export function DebugPage({navigation}: PropsWithNavigation) {
  const dispatch = useAppDispatch();

  const logout = async () => {
    await AuthTokenService.deleteToken();
    dispatch(setAuthorized(false));
  };

  const showToken = async () => {
    const token = await AuthTokenService.getToken();
    console.log('Current token: ');
    console.log(token);
  };

  const toMain = () => {
    navigation.navigate('MainChildren');
  };

  const toNutrition = () => {
    navigation.navigate('Nutrition');
  };

  return (
    <View style={{display: 'flex', gap: 16}}>
      <Text>Отладка</Text>
      <ButtonPrimary title={'Выйти из аккаунта'} onPress={logout}/>
      <ButtonPrimary title={'Вывести токен в консоль'} onPress={showToken}/>
      <Text>Экраны</Text>
      <ButtonPrimary title={'На главную'} onPress={toMain}/>
      <ButtonPrimary title={'Питание'} onPress={toNutrition}/>
    </View>
  );
}
