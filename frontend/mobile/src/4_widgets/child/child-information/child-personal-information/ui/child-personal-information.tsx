import {ChildPersonalInformationProps} from "../model/props";
import {TitleText} from "../../../../../7_shared/ui/text/title-text/title.text";
import {ButtonPrimary} from "../../../../../7_shared/ui/buttons/button-primary";
import {ChildAccount} from "../../../child-account/ui/child-account";
import {TagsInformation} from "../../tags-informations/ui/tags-information";
import {View} from "react-native";
import {createStyle} from "../consts/style";

export function ChildPersonalInformation(props: ChildPersonalInformationProps) {
    const styles = createStyle(props);

    const navigateNutritionPage = () => {

    };

    return (
        <View style={styles.container}>
            <TitleText title={`${props.childInformation.firstName} ${props.childInformation.lastName}`}/>
            <ChildAccount balance={props.childInformation.balance}/>
            <TagsInformation
                class={`${props.childInformation.schoolClass.number}${props.childInformation.schoolClass.letter.toUpperCase()}`}
                school={props.childInformation.schoolClass.school.name}
                status={'Питается платно'}/>
            <ButtonPrimary
                title={'Питание'}
                onPress={navigateNutritionPage}
                backgroundColor={'#EC662A'}
                textColor={'#FFFFFF'}
                borderRadius={10}/>
        </View>
    );
}
