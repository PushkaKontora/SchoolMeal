import {MarginArea} from '../../../7_shared/ui/styling/margin-area';
import {SUB_EMOJI_TITLE} from '../consts/consts';
import {ButtonPrimary} from '../../../7_shared/ui/buttons/button-primary/button-primary';
import {EmojiTextFeature} from '../../../5_features/emoji-text-feature/ui/emoji-text-feature';
import {PaddingArea} from '../../../7_shared/ui/styling/padding-area/padding-area';

export function AddChildrenWidget() {
  const navigateToSignUp = () => {

  };

  return (
    <EmojiTextFeature
      imageEmoji={require('../../../5_features/emoji-text-feature/images/angelAmoji.png')}
      subEmojiTitle={SUB_EMOJI_TITLE}>
      <ButtonPrimary
        title={'Добавить ребёнка'}
        onPress={navigateToSignUp}
        backgroundColor={'#EC662A'}
        textColor={'#FFFFFF'}
        borderRadius={10}/>
    </EmojiTextFeature>
  );
}
