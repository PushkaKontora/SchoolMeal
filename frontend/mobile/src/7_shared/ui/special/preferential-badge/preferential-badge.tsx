import {PreferentialBadgeProps} from './props';
import {Text, View} from 'react-native';
import {styles} from './styles';

export function PreferentialBadge(props: PreferentialBadgeProps) {
  return (
    <View style={styles.background}>
      <View
        style={styles.active}>
        <Text
          style={styles.activeText}>
          {props.title}
        </Text>
      </View>
    </View>
  );
}
