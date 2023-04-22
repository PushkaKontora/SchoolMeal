import {HorizontalLineProps} from './props';
import {View} from 'react-native';
import {createStyle} from './style';

export function HorizontalLine(props: HorizontalLineProps) {
  return (
    <View
      style={createStyle(props).default}/>
  );
}
