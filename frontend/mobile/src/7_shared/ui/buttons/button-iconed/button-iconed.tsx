import {TouchableOpacity} from 'react-native';
import {Icon} from '../../special/icon';
import {ButtonIconedProps} from './props';

export function ButtonIconed(props: ButtonIconedProps) {
  return (
    <TouchableOpacity
      onPress={props.onPress}>
      <Icon
        size={props.size}
        resource={props.resource}/>
    </TouchableOpacity>
  );
}
