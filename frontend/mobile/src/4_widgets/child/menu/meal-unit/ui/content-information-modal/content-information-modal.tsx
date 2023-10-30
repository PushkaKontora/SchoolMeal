import {Image, ImageBackground, Text, View} from 'react-native';
import {ContentInformationModalProps} from './props';
import {createStyle} from './style';

export function ContentInformationModal(props: ContentInformationModalProps) {
  const styles = createStyle();

  return (
    <View style={styles.container}>
      <View style={styles.containerMainInfo}>
        <View style={styles.containerImage}>
          <ImageBackground source={require('../../../../../../7_shared/assets/images/Rectangle.png')}
            style={{width: '100%', height: '100%'}}>
            <View style={{flex: 1}}>
              <Image style={styles.image}
                source={props.imagePath}
              />
            </View>
          </ImageBackground>
        </View>
        <View style={styles.containerMainText}>
          <Text style={styles.priceText}>
            {props.portions.price}₽
          </Text>
          <Text style={styles.weightText}>
            {props.portions.weight}г
          </Text>
        </View>
      </View>
      <View style={styles.containerDetailComposition}>
        <View>
          <Text style={styles.item}>{props.portions.kcal}</Text>
          <Text style={styles.nameItem}>ккал</Text>
        </View>
        <View>
          <Text style={styles.item}>{props.portions.protein}</Text>
          <Text style={styles.nameItem}>белки</Text>
        </View>
        <View>
          <Text style={styles.item}>{props.portions.fats}</Text>
          <Text style={styles.nameItem}>жиры</Text>
        </View>
        <View>
          <Text style={styles.item}>{props.portions.carbs}</Text>
          <Text style={styles.nameItem}>углеводы</Text>
        </View>
      </View>
      <View>
        <Text style={styles.nameCompound}>Состав</Text>
        <Text style={styles.compound}>{props.portions.components}</Text>
      </View>
    </View>
  );
}
