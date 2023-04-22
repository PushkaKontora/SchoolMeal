import {PaddingAreaProps} from './props';
import {View} from 'react-native';
import {createStyle} from './style';

export function PaddingArea({children, style, ...paddings}: PaddingAreaProps) {
  const styles = createStyle({...style, ...paddings});

  return (
    <View
      style={styles.default}>
      {children}
    </View>
  );
}
