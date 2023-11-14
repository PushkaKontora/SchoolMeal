import {createStyle} from '../config/styles';
import {Text, View} from 'react-native';
import {TypedToastProps} from '../model/props';

export function ToastView(props: TypedToastProps) {
  const styles = createStyle(props);

  return (
    <View style={styles.toastContainer}>
      <View style={styles.textContainer}>
        <Text style={styles.title}>
          {props.data.title}
        </Text>
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
