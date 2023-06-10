import {MenuDataProps} from '../model/props';
import {View} from 'react-native';
import {createStyle} from "../consts/style";
import {TitleText} from "../../../../../7_shared/ui/text/title-text/title.text";
import {MiniCalendar} from "../../../../../7_shared/ui/special/mini-calendar";
import {setDataMenu} from "../../menu/model/menu-slice/menu-slice";
import {useAppDispatch} from "../../../../../../store/hooks";

export function MenuData(props: MenuDataProps) {
    const styles = createStyle(props);
    const dispatch = useAppDispatch()
    const handlerClickDate = (date: any) => {
        dispatch(setDataMenu(date.toString()));
        console.log(date, 'MenuData')
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
