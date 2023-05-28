import {Text, View} from 'react-native';
import {TitleTextProps} from './props';
import {createStyle} from './style';

export function TitleText(props: TitleTextProps) {

    const styles = createStyle(props);

    return (
        <View style={styles.container}>
            <Text style={styles.default}>
                {props.title}
            </Text>
        </View>
    );
}
