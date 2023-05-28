import {View} from 'react-native';
import {MenuProps} from '../model/props';
import {createStyle} from '../consts/style';
import {MenuData} from '../../menu-data/ui/menu-data';
import {MealUnit} from '../../meal-unit/ui/meal-unit';
import {Portions} from '../../../../../7_shared/model/portions';
import {ButtonPrimary} from '../../../../../7_shared/ui/buttons/button-primary';

export function Menu(props: MenuProps) {

  const styles = createStyle(props);

  const handleLeaveFeedback = () => {

  };
  return (
    <View style={styles.container}>
      <MenuData/>
      {props.meals.menu.breakfast
                && <MealUnit title={'Завтрак'}
                  sum={'100'}
                  portions={portions.portions}/>}
      {props.meals.menu.dinner
                && <MealUnit title={'Обед'}
                  sum={'100'}
                  portions={portions.portions}/>}
      {props.meals.menu.lunch
              && <MealUnit title={'Полдник'}
                sum={'100'}
                portions={portions.portions}/>}
      <ButtonPrimary
        title={'Оставить отзыв'}
        onPress={handleLeaveFeedback}
        backgroundColor={'#EC662A'}
        textColor={'#FFFFFF'}
        borderRadius={100}/>
    </View>
  );
}


const portions: { portions: Portions[] } = {
  'portions': [
    {
      'id': 0,
      'food': {
        'id': 0,
        'schoolId': 0,
        'name': 'Каша рисовая с маслом',
        'photoPath': 'string'
      },
      'components': 'Рисовая крупа, молоко 2,5%, сахар, соль, масло сливочное',
      'weight': 250,
      'kcal': 345,
      'protein': 5.1,
      'fats': 8,
      'carbs': 19.2,
      price: 100
    },
    {
      'id': 2,
      'food': {
        'id': 0,
        'schoolId': 0,
        'name': 'Яблоко',
        'photoPath': 'string'
      },
      'components': 'Рисовая крупа, молоко 2,5%, сахар, соль, масло сливочное',
      'weight': 60,
      'kcal': 345,
      'protein': 5.1,
      'fats': 8,
      'carbs': 19.2,
      price: 100
    }
  ]
};