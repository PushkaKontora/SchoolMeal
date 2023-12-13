import {ChildPersonalInformationProps} from '../model/props';
import {TitleText} from '../../../../../7_shared/ui/text/title-text/title.text';
import {ButtonPrimary} from '../../../../../7_shared/ui/buttons/button-primary';
import {ChildAccount} from '../../../child-account/ui/child-account';
import {TagsInformation} from '../../tags-informations/ui/tags-information';
import {View} from 'react-native';
import {createStyle} from '../consts/style';
import {useEffect, useState} from 'react';

export function ChildPersonalInformation(props: ChildPersonalInformationProps) {
  const styles = createStyle();
  const [status, setStatus]
    = useState(props.childInformation.mealPlan.status);
  const {navigation} = props;

  useEffect(() => {
    setStatus(props.childInformation.mealPlan.status);
  }, [props.childInformation]);

  const navigateNutritionPage = () => {
    navigation.navigate('Nutrition', {
      childId: props.childInformation.id
    });
  };

  return (
    <View style={styles.container}>
      <TitleText title={`${props.childInformation.firstName} ${props.childInformation.lastName}`}/>
      <ChildAccount balance={0}/>
      <TagsInformation
        class={`${props.childInformation.schoolClass.number}${props.childInformation.schoolClass.literal.toUpperCase()}`}
        school={props.childInformation.schoolClass.school.name}
        status={status}/>
      <ButtonPrimary
        title={'Поставить на питание'}
        onPress={navigateNutritionPage}
        backgroundColor={'#EC662A'}
        textColor={'#FFFFFF'}
        borderRadius={10}/>
    </View>
  );
}

