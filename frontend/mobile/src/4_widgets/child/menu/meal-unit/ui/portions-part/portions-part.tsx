import {Image, ImageBackground, Text, TouchableOpacity, View} from 'react-native';
import {PortionsPartProps} from './props';
import {createStyle} from './style';
import {magicModal} from 'react-native-magic-modal';
import {InformationModal} from './infomation-modal';

export function PortionsPart(props: PortionsPartProps) {
  const styles = createStyle();

  const createInfoModal = () => {
    return (<InformationModal styles={styles} onExit={clickExit} {...props}/>);
  };

  const openInformationPortions = () => {
    return magicModal.show(createInfoModal);
  };

  const clickExit = (): void => {
    magicModal.hide();
  };

  return (
    <TouchableOpacity onPress={openInformationPortions}
      style={styles.container}>
      <View style={styles.container}>
        <View style={styles.imageContainer}>
          <ImageBackground source={require('../../../../../../7_shared/assets/images/Rectangle.png')}
            style={{width: '100%', height: '100%'}}>
            <Image source={props.imagePath} style={styles.image}/>
          </ImageBackground>
        </View>
        <View style={styles.textContainer}>
          <Text style={styles.textPart}>{props.portions.food.name}</Text>
          <Text style={styles.textPart}>{props.portions.weight} г</Text>
        </View>
      </View>
    </TouchableOpacity>
  );
}
