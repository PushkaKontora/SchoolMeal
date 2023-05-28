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
      <Menu meals={meals}/>
    </ScrollView>
  );
}

const meals = {
  'id': 0,
  'classId': 0,
  'date': '2023-05-21',
  'menu': {
    'breakfast': {
      'price': 0,
      'portions': [
        {
          'id': 0,
          'food': {
            'id': 0,
            'schoolId': 0,
            'name': 'Каша рисовая с маслом',
            'photoPath': 'string'
          },
          'components': 'Рисовая крупа, молоко 2,5%, сахар, соль, масло сливочное',
          'weight': 250,
          'kcal': 345,
          'protein': 5.1,
          'fats': 8,
          'carbs': 19.2,
          price: 100
        },
        {
          'id': 2,
          'food': {
            'id': 0,
            'schoolId': 0,
            'name': 'Яблоко',
            'photoPath': 'string'
          },
          'components': 'Рисовая крупа, молоко 2,5%, сахар, соль, масло сливочное',
          'weight': 60,
          'kcal': 345,
          'protein': 5.1,
          'fats': 8,
          'carbs': 19.2,
          price: 100
        }
      ]
    },
    'lunch': {
      'price': 0,
      'portions': [
        {
          'id': 0,
          'food': {
            'id': 0,
            'schoolId': 0,
            'name': 'Каша рисовая с маслом',
            'photoPath': 'string'
          },
          'components': 'Рисовая крупа, молоко 2,5%, сахар, соль, масло сливочное',
          'weight': 250,
          'kcal': 345,
          'protein': 5.1,
          'fats': 8,
          'carbs': 19.2,
          price: 100
        },
        {
          'id': 2,
          'food': {
            'id': 0,
            'schoolId': 0,
            'name': 'Яблоко',
            'photoPath': 'string'
          },
          'components': 'Рисовая крупа, молоко 2,5%, сахар, соль, масло сливочное',
          'weight': 60,
          'kcal': 345,
          'protein': 5.1,
          'fats': 8,
          'carbs': 19.2,
          price: 100
        }
      ]
    },
    'dinner': {
      'price': 0,
      'portions': [
        {
          'id': 0,
          'food': {
            'id': 0,
            'schoolId': 0,
            'name': 'Каша рисовая с маслом',
            'photoPath': 'string'
          },
          'components': 'Рисовая крупа, молоко 2,5%, сахар, соль, масло сливочное',
          'weight': 250,
          'kcal': 345,
          'protein': 5.1,
          'fats': 8,
          'carbs': 19.2,
          price: 100
        },
        {
          'id': 2,
          'food': {
            'id': 0,
            'schoolId': 0,
            'name': 'Яблоко',
            'photoPath': 'string'
          },
          'components': 'Рисовая крупа, молоко 2,5%, сахар, соль, масло сливочное',
          'weight': 60,
          'kcal': 345,
          'protein': 5.1,
          'fats': 8,
          'carbs': 19.2,
          price: 100
        }
      ]
    },
  }
};
