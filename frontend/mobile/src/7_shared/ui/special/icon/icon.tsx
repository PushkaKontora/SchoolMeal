import {IconProps} from './props';
import {createStyle} from './styles';
import {Image} from 'react-native';

export function Icon(props: IconProps) {
  const styles = props.size ? createStyle(props.size).iconContainer : {};

  return (
    <Image
      source={props.resource}
      style={styles}/>
  );
}
