import {View} from 'react-native';
import {MenuProps} from "../model/props";
import {createStyle} from "../consts/style";
import {MenuData} from "../../menu-data/ui/menu-data";
import {MealUnit} from "../../meal-unit/ui/meal-unit";
import {Portions} from "../../../../../7_shared/model/portions";
import {useAppSelector} from "../../../../../../store/hooks";
import {useEffect} from "react";
import {useGetMealsQuery} from "../../../../../6_entities/meal/api/meal-api/config";
import {EmojiTextFeature} from "../../../../../5_features/emoji-text-feature/ui/emoji-text-feature";

export function Menu(props: MenuProps) {
    const date = useAppSelector((state) => state.menu.dateMeal);
    const styles = createStyle(props);
    const {data: mealsForChild, refetch} = useGetMealsQuery({classId: props.classId, dateFrom: date, dateTo: date})

    useEffect(() => {
        refetch;
        if (mealsForChild) {
            console.log(mealsForChild[0], 55)
        }
    }, [date])

    return (
        <View style={styles.container}>
            <MenuData/>
            {mealsForChild && mealsForChild[0]?.menu?.breakfast
                && <MealUnit title={'Завтрак'}
                             sum={mealsForChild[0]?.menu?.breakfast.price}
                             portions={mealsForChild[0].menu.breakfast.portions}/>}
            {mealsForChild && mealsForChild[0]?.menu?.lunch
                && <MealUnit title={'Полдник'}
                             sum={mealsForChild[0]?.menu?.lunch.price}
                             portions={mealsForChild[0].menu.lunch.portions}/>}
            {mealsForChild && mealsForChild[0]?.menu?.dinner
                && <MealUnit title={'Обед'}
                             sum={mealsForChild[0]?.menu?.dinner.price}
                             portions={mealsForChild[0].menu.dinner.portions}/>}
            <EmojiTextFeature
                imageEmoji={require('../lib/assets/Object.png')}
                subEmojiTitle={'На этот день меню не было предоставлено'}/>
            {/*<ButtonPrimary*/}
            {/*    title={'Оставить отзыв'}*/}
            {/*    onPress={handleLeaveFeedback}*/}
            {/*    backgroundColor={'#EC662A'}*/}
            {/*    textColor={'#FFFFFF'}*/}
            {/*    borderRadius={100}/>*/}
        </View>
    );
}

// const portions: { portions: Portions[] } = {
//     "portions": [
//         {
//             "id": 0,
//             "food": {
//                 "id": 0,
//                 "schoolId": 0,
//                 "name": "Каша рисовая с маслом",
//                 "photoPath": "string"
//             },
//             "components": "Рисовая крупа, молоко 2,5%, сахар, соль, масло сливочное",
//             "weight": 250,
//             "kcal": 345,
//             "protein": 5.1,
//             "fats": 8,
//             "carbs": 19.2,
//             price: 100
//         },
//         {
//             "id": 2,
//             "food": {
//                 "id": 0,
//                 "schoolId": 0,
//                 "name": "Яблоко",
//                 "photoPath": "string"
//             },
//             "components": "Рисовая крупа, молоко 2,5%, сахар, соль, масло сливочное",
//             "weight": 60,
//             "kcal": 345,
//             "protein": 5.1,
//             "fats": 8,
//             "carbs": 19.2,
//             price: 100
//         }
//     ]
// };