import {View} from 'react-native';
import {MealUnitProps} from '../model/props';
import {createStyle} from '../consts/style';
import {TitleText} from '../../../../../7_shared/ui/text/title-text/title.text';
import {PortionsPart} from './portions-part/portions-part';

export function MealUnit(props: MealUnitProps) {
  const styles = createStyle();

  return (
    <View style={styles.container}>
      <View style={styles.title}>
        <TitleText title={props.title}/>
        <TitleText textColor={'#E9632C'}
          fontSize={12}
          lineHeight={24}
          title={`${props.sum} ₽`}
          marginLeft={'auto'}/>
      </View>
      {props?.portions.map(por =>
        <PortionsPart key={por.id}
          //imagePath={require('../../../../../7_shared/assets/images/Rectangle.png')}
          //imagePath={por.food.photoPath}
          imagePath={{
            'uri': por.food?.photoPath
          }}
          portions={por}/>)}
    </View>
  );
}
