import {StatusBar, Text, View} from 'react-native';
import {ButtonIconed} from '../../../7_shared/ui/buttons/button-iconed';
import {AppHeaderProps} from '../types/props';
import {styles} from '../consts/styles';

export function AppHeader(props: AppHeaderProps) {
  const onBackPressed = () => {
    props.navigation.goBack();
  };

  return (
    <View
      style={styles.container}>
      <StatusBar
        barStyle={'light-content'}/>
      <View
        style={styles.body}>

        {
          props.showBackButton && (
            <View
              style={styles.back}>
              <ButtonIconed
                onPress={onBackPressed}
                size={20}
                resource={require('../../../../assets/arrow-back.png')}/>
            </View>
          )
        }

        <Text
          style={styles.title}>
          {props.title}
        </Text>

        <View
          style={styles.children}>
          {props.children}
        </View>

      </View>
    </View>
  );
}
