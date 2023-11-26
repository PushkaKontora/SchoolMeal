import {Text} from 'react-native';
import {ErrorMessageProps} from './props';
import {createStyle} from './style';

export function TextErrorMessage(props: ErrorMessageProps) {
  const styles = createStyle(props);

  return (
    <Text style={styles.errorMessage}>
      {props.textMessage}
    </Text>
  );
}
