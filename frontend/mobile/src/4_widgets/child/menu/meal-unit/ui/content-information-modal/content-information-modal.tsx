import {Image, Text, View} from 'react-native';
import {ContentInformationModalProps} from './props';
import {createStyle} from './style';
import {TitleText} from "../../../../../../7_shared/ui/text/title-text/title.text";

export function ContentInformationModal(props: ContentInformationModalProps) {
    const styles = createStyle(props);

    return (
        <View style={styles.container}>
            <View style={styles.containerMainInfo}>
                <View style={styles.containerImage}>
                    <Image style={styles.image}
                           source={props.imagePath}/>
                </View>
                <View style={styles.containerMainText}>
                    <Text style={styles.priceText}>
                        {props.portions.price}₽
                    </Text>
                    <Text style={styles.weightText}>
                        {props.portions.weight}г
                    </Text>
                </View>
            </View>
            <View style={styles.containerDetailComposition}>
                <View>
                    <Text style={styles.item}>{props.portions.kcal}</Text>
                    <Text style={styles.nameItem}>ккал</Text>
                </View>
                <View>
                    <Text style={styles.item}>{props.portions.protein}</Text>
                    <Text style={styles.nameItem}>белки</Text>
                </View>
                <View>
                    <Text style={styles.item}>{props.portions.fats}</Text>
                    <Text style={styles.nameItem}>жиры</Text>
                </View>
                <View>
                    <Text style={styles.item}>{props.portions.carbs}</Text>
                    <Text style={styles.nameItem}>углеводы</Text>
                </View>
            </View>
            <View>
                <Text style={styles.nameCompound}>Состав</Text>
                <Text style={styles.compound}>{props.portions.components}</Text>
            </View>
        </View>
    );
}
