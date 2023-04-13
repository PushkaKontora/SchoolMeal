import {PaddingAreaProps} from './props';
import {View} from 'react-native';
import {createStyle} from './style';

export function PaddingArea({children, ...paddings}: PaddingAreaProps) {
  const styles = createStyle(paddings);

  return (
    <View
      style={styles.default}>
      {children}
    </View>
  );
}
