import {ChildInformationProps} from '../model/props';
import {
  ChildPersonalInformation
} from '../../../4_widgets/child/child-information/child-personal-information/ui/child-personal-information';
import {Menu} from '../../../4_widgets/child/menu/menu/ui/menu';
import {ScrollView} from 'react-native';

export function ChildInformationPage({route, navigation}: ChildInformationProps) {
  return (
    <ScrollView>
      <ChildPersonalInformation childInformation={route.params.childInformation}
        navigation={navigation}/>
      <Menu classId={route.params.childInformation.schoolClass.id}/>
    </ScrollView>
  );
}
