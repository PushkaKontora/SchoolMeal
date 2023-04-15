import {Text, View} from 'react-native';
import {AuthFeatureProps} from '../model/props';
import {createStyle} from '../consts/style';
import {PaddingArea} from '../../../7_shared/ui/styling/padding-area';
import {PADDINGS} from '../config/config';

export function AuthFeature(props: AuthFeatureProps) {
  const styles = createStyle(props);

  return (
    <PaddingArea
      style={styles.container}
      {...PADDINGS}>
      <View style={styles.titles}>
        <Text style={styles.header}>{props.headerTitle}</Text>
        <Text style={styles.subHeader}>{props.subHeaderTitle}</Text>
      </View>

      {props.children}
    </PaddingArea>

  );
}
