import {ChildAccountProps} from '../model/props';
import {Image, Text, View} from 'react-native';
import {createStyle} from '../consts/style';
import {ButtonPrimary} from '../../../../7_shared/ui/buttons/button-primary';

export function ChildAccount(props: ChildAccountProps) {
  const styles = createStyle();

  return (
    <View style={styles.container}>
      <View>
        <Image source={require('../../../../7_shared/assets/images/replenish.png')}/>
      </View>
      <View style={styles.containerContent}>
        <Text style={styles.content}>{props.balance}</Text>
        <Text style={styles.contentRuble}>₽</Text>
      </View>
      <View style={styles.containerButton}>
        <ButtonPrimary
          title={'Пополнить'}
          backgroundColor={'#EC662A'}
          textColor={'#FFFFFF'}
          borderRadius={100}
          fontSize={11}
          paddingVertical={6}
          paddingHorizontal={12}/>
      </View>
    </View>
  );
}
