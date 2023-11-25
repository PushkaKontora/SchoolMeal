import {EmojiTextFeature} from '../../../../../5_features/emoji-text-feature/ui/emoji-text-feature';
import HeartIcon from '../../../../../7_shared/assets/images/heart_feedback.svg';

export function SuccessFeedback() {
  return (
    <EmojiTextFeature
      gap={4}
      paddings={{
        paddingTop: 9,
        paddingBottom: 12,
        paddingHorizontal: 16
      }}
      svgComponent={<HeartIcon width={92} height={92}/>}
      subEmojiTitle={'Ваш отзыв успешно\nотправлен'}/>
  );
}
