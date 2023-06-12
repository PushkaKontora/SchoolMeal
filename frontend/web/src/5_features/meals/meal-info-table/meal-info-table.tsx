import {MealInfoTableProps} from './props';
import {Table} from './styles';
import {MealThreeColumnHeader} from '../../../6_entities/meals/ui/meal-three-column-header';
import {MealTableValueCell} from '../../../6_entities/meals/ui/meal-table-value-cell/meal-table-value-cell';
import {FOOTER_ROW_STYLES} from './config';

export function MealInfoTable(props: MealInfoTableProps) {
  return (
    <Table
      width={props.width}>
      <MealThreeColumnHeader
        mealName={'Завтрак'}/>
      <MealTableValueCell
        paid={'8'}
        preferential={'1'}
        total={'9'}/>
      <MealTableValueCell
        paid={'8'}
        preferential={'1'}
        total={'9'}/>
      <MealTableValueCell
        paid={'8'}
        preferential={'1'}
        total={'9'}/>
      <MealTableValueCell
        backgroundColor={FOOTER_ROW_STYLES.backgroundColor}
        paid={'8'}
        preferential={'1'}
        total={'9'}/>
    </Table>
  );
}
