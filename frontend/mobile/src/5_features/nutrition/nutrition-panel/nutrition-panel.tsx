import {Text, View} from 'react-native';
import {styles} from './styles';
import {MiniCalendar} from '../../../7_shared/ui/special/mini-calendar/mini-calendar';
import {EmojiTextFeature} from '../../emoji-text-feature/ui/emoji-text-feature';
import {ButtonSecondary} from '../../../7_shared/ui/buttons/button-secondary/button-secondary';

export function NutritionPanel() {
  return (
    <View
      style={styles.container}>
      <Text
        style={styles.title}>
        {'Снять с питания'}
      </Text>

      <Text
        style={styles.description}>
        {'Выберите дни, когда ребенка не будет в школе (не будет питаться)'}
      </Text>
      
      <MiniCalendar selectionColor={'#EE6725'} itemNumber={5}/>

      <View>
        <EmojiTextFeature
          imageEmoji={require('../../../5_features/emoji-text-feature/images/happy_emoji.png')}
          subEmojiTitle={'Ваш ребенок питается в этот день'}/>
      </View>

      <ButtonSecondary
        title={'Снять с питания'}
        onPress={() => {return;}}
        borderRadius={10}
        borderColor={'#E9632C'}
        textColor={'#E9632C'}/>
    </View>
  );
}
