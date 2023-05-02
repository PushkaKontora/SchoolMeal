import {SignUpProps} from '../../../3_pages/sign-up-page/model/props';
import {AuthFeature} from '../../../5_features/auth-feature/ui/auth-feature';
import {HEADER_TITLE, SUBHEADER_TITLE} from '../consts/consts';
import {MarginArea} from '../../../7_shared/ui/styling/margin-area';
import {HorizontalLine} from '../../../7_shared/ui/styling/horizontal-line';
import {ButtonSecondary} from '../../../7_shared/ui/buttons/button-secondary/button-secondary';
import {SignUpForm} from '../../../6_entities/user/ui/sign-up-form';

export function SignUpWidget({navigation}: SignUpProps) {
  const navigateToLogin = () => {
    navigation.goBack();
  };

  return (
    <AuthFeature
      headerTitle={HEADER_TITLE}
      subHeaderTitle={SUBHEADER_TITLE}>

      <MarginArea
        marginBottom={16}>

        <SignUpForm/>

      </MarginArea>

      <MarginArea
        marginBottom={16}>
        <HorizontalLine/>
      </MarginArea>

      <ButtonSecondary title={'Вход'} onPress={navigateToLogin}/>

    </AuthFeature>
  );
}