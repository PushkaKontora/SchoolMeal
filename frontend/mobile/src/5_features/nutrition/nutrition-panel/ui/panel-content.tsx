import {View} from 'react-native';
import {EmojiTextFeature} from '../../../emoji-text-feature/ui/emoji-text-feature';
import {ButtonSecondary} from '../../../../7_shared/ui/buttons/button-secondary/button-secondary';
import {SELECTION_COLOR} from '../config/config';
import {PanelContentProps} from '../types/props';

export function PanelContent(props: PanelContentProps) {
  return (
    <View>
      <View>
        <EmojiTextFeature
          imageEmoji={props.emojiImage}
          subEmojiTitle={props.subEmojiTitle}/>
      </View>

      <ButtonSecondary
        title={props.buttonTitle}
        onPress={props.onButtonPress}
        borderRadius={10}
        borderColor={SELECTION_COLOR}
        textColor={SELECTION_COLOR}/>
    </View>
  );
}
