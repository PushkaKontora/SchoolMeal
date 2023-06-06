import {View} from 'react-native';
import {EmojiTextFeature} from '../../../emoji-text-feature/ui/emoji-text-feature';
import {ButtonSecondary} from '../../../../7_shared/ui/buttons/button-secondary/button-secondary';
import {SELECTION_COLOR} from '../config/config';
import {PanelContentProps} from '../types/props';
import {styles} from '../consts/styles';
import {useEffect, useState} from 'react';
import {setVisibilityDefaultValue} from '../lib/panel-utils';

export function PanelContent(props: PanelContentProps) {
  const [buttonVisibility, setButtonVisibility] = useState(setVisibilityDefaultValue(props.visibleButton));

  useEffect(() => {
    setButtonVisibility(setVisibilityDefaultValue(props.visibleButton));
  }, [props.visibleButton]);

  return (
    <View
      style={styles.emojiContainer}>
      <View>
        <EmojiTextFeature
          imageEmoji={props.emojiImage}
          subEmojiTitle={props.subEmojiTitle}/>
      </View>

      {
        buttonVisibility &&
        <ButtonSecondary
          title={props.buttonTitle}
          onPress={props.onButtonPress}
          borderRadius={10}
          borderColor={SELECTION_COLOR}
          textColor={SELECTION_COLOR}/>
      }
    </View>
  );
}
