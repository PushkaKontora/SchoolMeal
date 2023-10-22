import {TagInformationProps} from './props';
import {Image, Text, View} from 'react-native';
import {createStyle} from './style';

export function TagInformation(props: TagInformationProps) {
  const styles = createStyle(props);

  return (
    <View style={styles.container}>
      {props.imageTag && <Image source={props.imageTag}/>}
      <Text numberOfLines={1}
        ellipsizeMode={'tail'}
        style={styles.titles}>{props.textTag}</Text>
    </View>
  );
}
