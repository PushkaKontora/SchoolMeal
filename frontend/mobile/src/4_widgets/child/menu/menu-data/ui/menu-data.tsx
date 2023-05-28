import {MenuDataProps} from '../model/props';
import {View} from 'react-native';
import {createStyle} from "../consts/style";
import {TitleText} from "../../../../../7_shared/ui/text/title-text/title.text";
import {MealUnit} from "../../meal-unit/ui/meal-unit";
import {MiniCalendar} from "../../../../../7_shared/ui/special/mini-calendar";

export function MenuData(props: MenuDataProps) {
    const styles = createStyle(props);

    const handlerClickDate = (date: Date) => {

    }

    return (
        <View style={styles.container}>
            <View>
                <TitleText title={'Меню'}/>
            </View>
            <MiniCalendar selectionColor={'#E9632C'}
                          onDateChange={handlerClickDate}/>
        </View>
    );
}
