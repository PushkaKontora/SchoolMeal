import {createStyle} from '../config/styles';
import {Text, View} from 'react-native';
import {TypedToastProps} from '../model/props';
import {ICONS} from '../config/icons';

export function ToastView(props: TypedToastProps) {
  const styles = createStyle(props);

  return (
    <View style={styles.toastContainer}>
      {
        props.type && ICONS[props.type]
      }

      <View style={styles.textContainer}>
        {
          props.data.title && (
            <Text style={styles.title}>
              {props.data.title}
            </Text>
          )
        }

        {
          props.data.description && (
            <Text style={styles.description}>
              {props.data.description}
            </Text>
          )
        }
      </View>
    </View>
  );
}
