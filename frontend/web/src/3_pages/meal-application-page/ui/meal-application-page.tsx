import {Sidebar, SidebarWithContent} from '../../../7_shared/ui/v2/sidebar';
import {PageStyles} from '../styles/page-styles.ts';
import {
  HeaderViewData,
  MealRequestList, MealRequestRowViewData
} from '../../../6_entities/meal-request';
import {useState} from 'react';
import {MealPlanHeaderCell} from '../../../6_entities/meal-plan/ui/meal-plan-header-cell';
import {updateDataState} from '../../../7_shared/lib/react-table-wrapper';

export function MealApplicationPage() {
  const [data, setData] = useState<MealRequestRowViewData[]>([
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: true,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: true,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    },
    {
      firstName: 'Мартына',
      lastName: 'Мартышкина',
      patronymic: 'Мартыновна',
      cancelledMeal: false,
      balance: 789.99,
      breakfast: true,
      dinner: false,
      snacks: true
    }
  ]);
  const [headerData, setHeaderData] = useState<HeaderViewData>({
    prices: {
      breakfast: 119.50,
      dinner: 249.99,
      snacks: 199.49
    }
  });

  return (
    <PageStyles>
      <SidebarWithContent
        sidebar={<Sidebar/>}>
        <div style={{
          margin: '16px'
        }}>
          <div style={{fontSize: 24, padding: 20}}>
            Текст
          </div>
          <MealRequestList
            data={data}
            headerViewData={headerData}
            cells={{
              mealPlanHeader: props => (
                <MealPlanHeaderCell
                  title={props.title}
                  price={props.price.toString()}/>
              )
            }}
            updateData={(rowIndex, columnKey, value) => {
              updateDataState(setData, rowIndex, columnKey, value);
            }}/>
        </div>
      </SidebarWithContent>
    </PageStyles>
  );
}
