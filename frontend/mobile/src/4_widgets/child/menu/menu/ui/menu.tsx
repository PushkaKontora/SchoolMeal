import {View} from 'react-native';
import {useAppSelector} from '../../../../../../store/hooks';
import {useEffect} from 'react';
import {MenuProps} from '../model/props';
import {createStyle} from '../consts/style';
import {MenuData} from '../../menu-data/ui/menu-data';
import {MealUnit} from '../../meal-unit/ui/meal-unit';
import {useGetMealsQuery} from '../../../../../6_entities/meal/api/meal-api/config';
import {EmojiTextFeature} from '../../../../../5_features/emoji-text-feature/ui/emoji-text-feature';

export function Menu(props: MenuProps) {
  const date = useAppSelector((state) => state.menu.dateMeal);
  const styles = createStyle(props);
  const {data: mealsForChild, refetch} = useGetMealsQuery({classId: props.classId, dateFrom: date, dateTo: date});

  useEffect(() => {
    (async () => {
      await refetch();
    })();
  }, [date]);

  return (
    <View style={styles.container}>
      <MenuData/>
      {mealsForChild && mealsForChild[0]?.menu?.breakfast
                && <MealUnit title={'Завтрак'}
                  sum={mealsForChild[0]?.menu?.breakfast.price}
                  portions={mealsForChild[0].menu.breakfast.portions}/>}
      {mealsForChild && mealsForChild[0]?.menu?.lunch
                && <MealUnit title={'Обед'}
                  sum={mealsForChild[0]?.menu?.lunch.price}
                  portions={mealsForChild[0].menu.lunch.portions}/>}
      {mealsForChild && mealsForChild[0]?.menu?.dinner
              && <MealUnit title={'Полдник'}
                sum={mealsForChild[0]?.menu?.dinner.price}
                portions={mealsForChild[0].menu.dinner.portions}/>}
      {mealsForChild && !mealsForChild[0]?.menu?.lunch
                && !mealsForChild[0]?.menu?.dinner
                && !mealsForChild[0]?.menu?.breakfast
                && <EmojiTextFeature
                  imageEmoji={require('../lib/assets/Object.png')}
                  subEmojiTitle={'На этот день меню не было предоставлено'}/>}

      {/*<EmojiTextFeature*/}
      {/*    imageEmoji={require('../lib/assets/Object.png')}*/}
      {/*    subEmojiTitle={'На этот день меню не было предоставлено'}/>*/}
      {/*<ButtonPrimary*/}
      {/*    title={'Оставить отзыв'}*/}
      {/*    onPress={handleLeaveFeedback}*/}
      {/*    backgroundColor={'#EC662A'}*/}
      {/*    textColor={'#FFFFFF'}*/}
      {/*    borderRadius={100}/>*/}
    </View>
  );
}
