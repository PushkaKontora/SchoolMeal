import {MarginAreaProps} from './props';
import {View} from 'react-native';
import {createStyle} from './style';

export function MarginArea({children, style, ...margins}: MarginAreaProps) {
  const styles = createStyle({...style, ...margins});

  return (
    <View
      style={styles.default}>
      {children}
    </View>
  );
}
