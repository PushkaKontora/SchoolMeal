import {Image, Text, View} from 'react-native';
import {EmojiTextProps} from '../model/props';
import {createStyle} from '../consts/style';
import {PaddingArea} from '../../../7_shared/ui/styling/padding-area';
import {PADDINGS} from '../config/config';

export function EmojiTextFeature(props: EmojiTextProps) {
  const styles = createStyle(props);

  return (
    <PaddingArea
      style={styles.container}
      {...PADDINGS}>
      <View style={styles.titles}>
        <Image source={props.imageEmoji}/>
        <Text style={styles.subEmoji}>{props.subEmojiTitle}</Text>
      </View>
      {props.children}
    </PaddingArea>
  );
}
