import {Image, Text, View} from 'react-native';
import {EmojiTextProps} from '../model/props';
import {createStyle} from '../consts/style';
import {PaddingArea} from '../../../7_shared/ui/styling/padding-area';
import {PADDINGS} from '../config/config';

export function EmojiTextFeature(props: EmojiTextProps) {
  const styles = createStyle(props);

  return (
    <PaddingArea
      {...PADDINGS}
      {...props.paddings}>
      <View style={styles.titles}>
        {props.imageEmoji && <Image style={styles.image} source={props.imageEmoji}/>}
        {!props.imageEmoji && props.svgComponent}
        <Text style={styles.subEmoji}>{props.subEmojiTitle}</Text>
      </View>
      {props.children}
    </PaddingArea>
  );
}
