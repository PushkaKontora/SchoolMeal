import {NutritionClassListWidget} from '../../../4_widgets/nutrition-class-list-widget';
import {useState} from 'react';
import {createClassNames} from '../../../6_entities/school-class';
import {toTableRowViewDataArray, toTableViewData} from '../lib/mappers.ts';
import {useAppSelector} from '../../../../store/hooks.ts';
import {updateDataState} from '../../../7_shared/lib/react-table-wrapper';
import {toSchoolClassArray} from '../../../7_shared/api/implementations/v3/mappers/school-class.ts';
import {toPupilArray} from '../../../7_shared/api/implementations/v3/mappers/pupil.ts';
import {PageStyles} from './styles.ts';
import {TitleWidget} from '../../../4_widgets/title-widget';
import {Switch} from '../../../7_shared/ui/v2/interactive/switch';
import {SwitchCell} from '../../../7_shared/ui/v2/table/cells/switch-cell';

export function NutritionClassListPage() {
  const userId = useAppSelector(state => state['auth'].jwtPayload?.user_id);

  const [classIndex, setClassIndex] = useState(0);

  /*
  const {data: classes} = Api.useGetSchoolClassesQuery({
    teacherId: userId!
  }, {skip: !userId});
  const {data: pupils} = Api.useGetPupilsQuery({
    classId: classes![classIndex].id
  }, {skip: !classes});
   */
  const classes = toSchoolClassArray(
    [
      {
        'id': '667432c2-0683-4f0f-bdb0-45aafbeb6ab8',
        'teacherId': 'a5958f26-02f6-4e5f-b0f2-c26f847aa2f6',
        'number': 1,
        'literal': 'И',
        'mealtimes': [
          'breakfast',
          'dinner',
          'snacks'
        ]
      },
      {
        'id': 'a588914e-1a9b-46c1-a8d5-2c015769bafd',
        'teacherId': 'a5958f26-02f6-4e5f-b0f2-c26f847aa2f6',
        'number': 2,
        'literal': 'И',
        'mealtimes': [
          'breakfast',
          'dinner'
        ]
      },
      {
        'id': '5bf741a9-5d12-462a-acc3-700685b19681',
        'teacherId': 'a5958f26-02f6-4e5f-b0f2-c26f847aa2f6',
        'number': 3,
        'literal': 'И',
        'mealtimes': [
          'breakfast',
          'snacks'
        ]
      },
      {
        'id': 'c1586334-a88a-497d-9f81-93a6e10b191e',
        'teacherId': 'a5958f26-02f6-4e5f-b0f2-c26f847aa2f6',
        'number': 4,
        'literal': 'И',
        'mealtimes': [
          'dinner',
          'snacks'
        ]
      },
      {
        'id': '1c2858f3-85b8-450d-9518-7c6b2e98dd75',
        'teacherId': 'a5958f26-02f6-4e5f-b0f2-c26f847aa2f6',
        'number': 5,
        'literal': 'И',
        'mealtimes': [
          'breakfast',
          'dinner',
          'snacks'
        ]
      },
      {
        'id': 'cc821ea2-e4b1-455b-84fc-74808038d020',
        'teacherId': 'a5958f26-02f6-4e5f-b0f2-c26f847aa2f6',
        'number': 6,
        'literal': 'И',
        'mealtimes': [
          'breakfast',
          'dinner'
        ]
      },
      {
        'id': '840203b5-108b-40b0-b399-eb5abd160b11',
        'teacherId': 'a5958f26-02f6-4e5f-b0f2-c26f847aa2f6',
        'number': 7,
        'literal': 'И',
        'mealtimes': [
          'breakfast',
          'snacks'
        ]
      },
      {
        'id': '3c198d35-0e05-4bc8-8129-1ceb5f391161',
        'teacherId': 'a5958f26-02f6-4e5f-b0f2-c26f847aa2f6',
        'number': 8,
        'literal': 'И',
        'mealtimes': [
          'dinner',
          'snacks'
        ]
      },
      {
        'id': '1c1b62aa-494b-4bef-9260-19eaa144036d',
        'teacherId': 'a5958f26-02f6-4e5f-b0f2-c26f847aa2f6',
        'number': 9,
        'literal': 'И',
        'mealtimes': [
          'breakfast',
          'dinner',
          'snacks'
        ]
      },
      {
        'id': '84c3ff06-d382-4cee-acc3-e2bbf63a80ae',
        'teacherId': 'a5958f26-02f6-4e5f-b0f2-c26f847aa2f6',
        'number': 10,
        'literal': 'И',
        'mealtimes': [
          'breakfast',
          'dinner'
        ]
      },
      {
        'id': '014fac13-1c98-450e-9a05-7f9ff53b764b',
        'teacherId': 'a5958f26-02f6-4e5f-b0f2-c26f847aa2f6',
        'number': 11,
        'literal': 'И',
        'mealtimes': [
          'breakfast',
          'snacks'
        ]
      }
    ]
  );
  const pupils = toPupilArray(
    [
      {
        'id': '04bbe7faa67b5a9641af',
        'classId': '667432c2-0683-4f0f-bdb0-45aafbeb6ab8',
        'parentIds': [
          '844c4372-52eb-4452-b314-728583ee5fbf'
        ],
        'lastName': 'Лыков',
        'firstName': 'Василий',
        'patronymic': 'Евгеньевич',
        'mealtimes': [
          'breakfast'
        ],
        'preferentialUntil': '2024-02-28',
        'cancelledPeriods': [],
        'nutrition': 'paid'
      },
      {
        'id': 'f488ef08b66bfa75adcc',
        'classId': '667432c2-0683-4f0f-bdb0-45aafbeb6ab8',
        'parentIds': [
          '844c4372-52eb-4452-b314-728583ee5fbf'
        ],
        'lastName': 'Перов',
        'firstName': 'Пётр',
        'patronymic': 'Владимирович',
        'mealtimes': [
          'dinner'
        ],
        'preferentialUntil': '2024-04-28',
        'cancelledPeriods': [],
        'nutrition': 'preferential'
      },
      {
        'id': '7dfbfd58a0f7fdda62db',
        'classId': '667432c2-0683-4f0f-bdb0-45aafbeb6ab8',
        'parentIds': [
          '844c4372-52eb-4452-b314-728583ee5fbf'
        ],
        'lastName': 'Самков',
        'firstName': 'Пётр',
        'patronymic': 'Евгеньевич',
        'mealtimes': [
          'snacks'
        ],
        'preferentialUntil': undefined,
        'cancelledPeriods': [],
        'nutrition': 'paid'
      },
      {
        'id': '3e68296c9fe85049cf19',
        'classId': '667432c2-0683-4f0f-bdb0-45aafbeb6ab8',
        'parentIds': [
          '844c4372-52eb-4452-b314-728583ee5fbf'
        ],
        'lastName': 'Сидоров',
        'firstName': 'Владимир',
        'patronymic': 'Дмитриевич',
        'mealtimes': [
          'breakfast',
          'dinner'
        ],
        'preferentialUntil': '2024-02-28',
        'cancelledPeriods': [],
        'nutrition': 'paid'
      },
      {
        'id': 'c42643ac58ef3783cb91',
        'classId': '667432c2-0683-4f0f-bdb0-45aafbeb6ab8',
        'parentIds': [
          '844c4372-52eb-4452-b314-728583ee5fbf'
        ],
        'lastName': 'Самков',
        'firstName': 'Пётр',
        'patronymic': undefined,
        'mealtimes': [
          'breakfast',
          'snacks'
        ],
        'preferentialUntil': '2024-04-28',
        'cancelledPeriods': [],
        'nutrition': 'preferential'
      }
    ]
  );

  const [tableData, setTableData]
    = useState(toTableRowViewDataArray(pupils));

  return (
    <PageStyles>
      <TitleWidget
        title={'Мои классы'}
        subtitle={'Здесь вы можете поставить ребенка на постоянное питание'}/>
      <NutritionClassListWidget
        data={tableData}
        tableData={toTableViewData(classes?.[classIndex].mealtimes)}
        updateData={(rowIndex, columnId, value) => {
          updateDataState(setTableData, rowIndex, columnId, value);
        }}
        selectedClassIndex={classIndex}
        classNames={createClassNames(classes)}
        onClassSelect={setClassIndex}/>
    </PageStyles>
  );
}
