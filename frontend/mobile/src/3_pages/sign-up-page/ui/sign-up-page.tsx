import {SignUpProps} from '../model/props';
import {SignUpWidget} from '../../../4_widgets/signup-widget';

export function SignUpPage({navigation}: SignUpProps) {
  return (
    <SignUpWidget
      navigation={navigation}/>
  );
}
