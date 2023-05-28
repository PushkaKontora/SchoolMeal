import {MenuDataProps} from '../model/props';
import {View} from 'react-native';
import {createStyle} from "../consts/style";
import {TitleText} from "../../../../../7_shared/ui/text/title-text/title.text";
import {MealUnit} from "../../meal-unit/ui/meal-unit";

export function MenuData(props: MenuDataProps) {
    const styles = createStyle(props);

    return (
        <View style={styles.container}>
            <View>
                <TitleText title={'Меню'}/>
            </View>
        </View>
    );
}
