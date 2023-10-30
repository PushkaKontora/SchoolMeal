import {TagsInformationProps} from '../model/props';
import {View} from 'react-native';
import {createStyle} from '../consts/style';
import {TagInformation} from '../../../child-card/ui/tag-information/tag-information';

export function TagsInformation(props: TagsInformationProps) {
  const styles = createStyle();

  return (
    <View style={styles.container}>
      <View style={styles.first}>
        <TagInformation paddingHorizontal={12}
          borderRadius={100}
          textTag={props.school}/>
        <TagInformation paddingHorizontal={12}
          borderRadius={100}
          textTag={props.class}/>

      </View>
      <View style={styles.second}>
        <TagInformation paddingHorizontal={12}
          borderRadius={100}
          textTag={props.status}/>
      </View>
    </View>
  );
}
