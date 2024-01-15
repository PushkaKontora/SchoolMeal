import {View} from 'react-native';
import {useAppSelector} from '../../../../../../store/hooks';
import {useEffect} from 'react';
import {MenuProps} from '../model/props';
import {createStyle} from '../consts/style';
import {MenuData} from '../../menu-data/ui/menu-data';
import {MealUnit} from '../../meal-unit/ui/meal-unit';
import {EmojiTextFeature} from '../../../../../5_features/emoji-text-feature/ui/emoji-text-feature';
import {ButtonPrimary} from '../../../../../7_shared/ui/buttons/button-primary';
import {magicModal} from 'react-native-magic-modal';
import {MenuFeedbackModal} from './menu-feedback-modal';
import {useGetMenuQuery} from '../../../../../6_entities/menu/api/api';

export function Menu(props: MenuProps) {
  const date = useAppSelector((state) => state.menu.dateMeal);

  const {data: mealsForChild, refetch} = useGetMenuQuery({
    schoolClassNumber: props.schoolClassNumber,
    date: date
  });

  const styles = createStyle();

  const openFeedbackModal = () => {
    magicModal.show(() => (
      <MenuFeedbackModal canteenId={props.schoolId}/>
    ));
  };

  useEffect(() => {
    (async () => {
      await refetch();
    })();
  }, [date]);

  return (
    <View style={styles.container}>
      <MenuData/>
      {mealsForChild && mealsForChild?.breakfast
                && <MealUnit title={'Завтрак'}
                  sum={mealsForChild?.breakfast.cost}
                  foods={mealsForChild.breakfast.foods}/>}
      {mealsForChild && mealsForChild?.dinner
                && <MealUnit title={'Обед'}
                  sum={mealsForChild.dinner.cost}
                  foods={mealsForChild.dinner.foods}/>}
      {mealsForChild && mealsForChild?.snacks
              && <MealUnit title={'Полдник'}
                sum={mealsForChild.snacks.cost}
                foods={mealsForChild.snacks.foods}/>}
      {(!mealsForChild || !mealsForChild?.breakfast
                || !mealsForChild?.dinner
                || !mealsForChild?.snacks)
                && <EmojiTextFeature
                  imageEmoji={require('../lib/assets/Object.png')}
                  subEmojiTitle={'На этот день меню не было предоставлено'}/>}

      <ButtonPrimary
        title={'Оставить отзыв'}
        onPress={openFeedbackModal}
        backgroundColor={'#EC662A'}
        textColor={'#FFFFFF'}
        borderRadius={100}
        fontSize={12}
        fontWeight={'700'}
        paddingVertical={9}/>
    </View>
  );
}
