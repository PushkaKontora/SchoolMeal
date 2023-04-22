import {AuthHeader} from '../../../../4_widgets/auth-header';
import {PropsWithNavigation} from '../../../../7_shared/model/props-with-navigation';
import {HEADER_TITLE} from '../consts/consts';

export function Header({navigation}: PropsWithNavigation) {
  return (
    <AuthHeader title={HEADER_TITLE} navigation={navigation}/>
  );
}
