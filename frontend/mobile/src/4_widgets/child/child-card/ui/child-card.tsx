import {ChildCardProps} from '../model/props';
import {Text, TouchableOpacity, View} from 'react-native';
import {ChildCardHeader} from '../../../../6_entities/child/ui/child-card-header/child-card-header';
import {TagInformation} from './tag-information/tag-information';
import {createStyle} from '../consts/style';

export function ChildCard(props: ChildCardProps) {
  const {navigation} = props;
  const handlerNavigateToChildPage = () => {
    navigation.navigate('ProfileChild', {childInformation: props.child});
  };

  const styles = createStyle(props);

  return (
    <TouchableOpacity
      onPress={handlerNavigateToChildPage}
      style={styles.container}>
      <ChildCardHeader
        ChildCardHeaderTitle={`${props.child.firstName} ${props.child.lastName}`}/>
      <View style={styles.content}>
        <View style={styles.tagContainer}>
          <TagInformation
            imageTag={require('../../../../7_shared/assets/images/map-pin.png')}
            textTag={props.child.schoolClass.school.name}/>
          <TagInformation
            imageTag={require('../../../../7_shared/assets/images/bell.png')}
            textTag={`${props.child.schoolClass.number} ${props.child.schoolClass.letter} класс`}/>
        </View>
        <View style={styles.statusMeal}>
          {props.child.certificateBeforeDate
                        && <Text style={styles.blueText}>Питается льготно</Text>}
          {!props.child.certificateBeforeDate
                        && (!props.child.dinner
                        && !props.child.lunch
                        && !props.child.breakfast
                          ? <Text style={styles.greyText}>Не питается</Text>
                          : <Text style={styles.greenText}>Питается платно</Text>)}
        </View>
      </View>
    </TouchableOpacity>
  );
}
