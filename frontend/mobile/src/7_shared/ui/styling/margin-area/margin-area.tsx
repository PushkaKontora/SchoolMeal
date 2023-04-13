import {MarginAreaProps} from './props';
import {View} from 'react-native';
import {createStyle} from './style';

export function MarginArea({children, ...margins}: MarginAreaProps) {
  const styles = createStyle(margins);

  return (
    <View
      style={styles.default}>
      {children}
    </View>
  );
}
