import {createStyle} from '../const/submitted-styles';
import {Text, View} from 'react-native';
import HeartFeedbackIcon from '../../../7_shared/assets/images/heart_feedback.svg';

export function ModalFeedbackSubmitted() {
  const styles = createStyle();

  return (
    <View
      style={styles.container}>
      <HeartFeedbackIcon
        width={92}
        height={92}/>
      <Text
        style={styles.successText}>
        {'Ваш отзыв успешно\n' +
          'отправлен'}
      </Text>
    </View>
  );
}
