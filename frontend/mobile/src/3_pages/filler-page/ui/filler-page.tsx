import {Text, View} from 'react-native';
import {MenuPageProps} from '../model/props';
import {ButtonPrimary} from '../../../7_shared/ui/buttons/button-primary';
import {AuthTokenService} from '../../../5_features/auth';
import {useAppDispatch} from '../../../../store/hooks';
import {setAuthorized} from '../../../5_features/auth/model/auth-slice/auth-slice';

export function FillerPage(props: MenuPageProps) {
  const dispatch = useAppDispatch();

  const logout = async () => {
    await AuthTokenService.deleteToken();
    dispatch(setAuthorized(false));
  };

  return (
    <View>
      <Text>Filler Page</Text>
      <ButtonPrimary title={'Выйти из аккаунта'} onPress={logout}/>
    </View>
  );
}
