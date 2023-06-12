import {TableContainer} from './styles';
import {MealClassTable} from '../../../5_features/meals/meal-class-table';
import {MealInfoTable} from '../../../5_features/meals/meal-info-table';
import {Content} from '../../../7_shared/ui/markup/content';

export function MealApplicationWidget() {
  return (
    <div>
      <Content>
        <TableContainer>
          <MealClassTable
            width={'25%'}/>

          <MealInfoTable
            width={'25%'}/>

          <MealInfoTable
            width={'25%'}/>

          <MealInfoTable
            width={'25%'}/>
        </TableContainer>
      </Content>
    </div>
  );
}
