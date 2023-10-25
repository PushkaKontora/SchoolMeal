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
  const [status, setStatus] = useState('Питается платно');
  const {navigation} = props;

  useEffect(() => {
    if (props.childInformation.certificateBeforeDate) {
      setStatus('Питается льготно');
    } else {
      if (!props.childInformation.dinner
                && !props.childInformation.lunch
                && !props.childInformation.breakfast) {
        setStatus('Не питается');
      } else {
        setStatus('Питается платно');
      }
    }
  });

  const navigateNutritionPage = () => {
    navigation.navigate('Nutrition', {
      childId: props.childInformation.id
    });
  };

  return (
    <View style={styles.container}>
      <TitleText title={`${props.childInformation.firstName} ${props.childInformation.lastName}`}/>
      <ChildAccount balance={props.childInformation.balance}/>
      <TagsInformation
        class={`${props.childInformation.schoolClass.number}${props.childInformation.schoolClass.letter.toUpperCase()}`}
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

//todo: изменить 26 строку на даныые  сервера
