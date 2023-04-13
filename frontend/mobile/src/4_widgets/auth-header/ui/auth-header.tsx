import {AuthHeaderProps} from '../model/props';
import {Text, View} from 'react-native';
import {STYLES} from '../consts/style';

export function AuthHeader(props: AuthHeaderProps) {
  return (
    <View style={STYLES.container}>
      <Text style={STYLES.headerText}>{props.title}</Text>
    </View>
  );
}
