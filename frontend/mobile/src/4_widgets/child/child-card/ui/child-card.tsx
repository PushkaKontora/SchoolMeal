import {ChildCardProps} from "../model/props";
import {Text, TouchableOpacity, View} from "react-native";
import {ChildCardHeader} from "../../../../6_entities/child/ui/child-card-header/child-card-header";
import {TagInformation} from "./tag-information/tag-information";
import {createStyle} from "../consts/style";

export function ChildCard(props: ChildCardProps) {
    const {
        navigation,
        nameChild,
        schoolAdress,
        classNumberAndLetter,
        certificateBeforeDate
    } = props;
    const handlerNavigateToChildPage = () => {
        navigation.navigate(props.childPagePath);
    }

    const styles = createStyle(props);


    return (
        <TouchableOpacity
            // onPress={handlerNavigateToChildPage}
            style={styles.container}>
            <ChildCardHeader ChildCardHeaderTitle={nameChild}/>
            <View style={styles.content}>
                <View style={styles.tagContainer}>
                    <TagInformation
                        imageTag={require('../../../../7_shared/assets/images/map-pin.png')}
                        textTag={schoolAdress}/>
                    <TagInformation
                        imageTag={require('../../../../7_shared/assets/images/bell.png')}
                        textTag={`${classNumberAndLetter} класс`}/>
                </View>
                <View style={styles.statusMeal}>
                    <Text>{certificateBeforeDate}</Text>
                </View>
            </View>
        </TouchableOpacity>
    );
}
