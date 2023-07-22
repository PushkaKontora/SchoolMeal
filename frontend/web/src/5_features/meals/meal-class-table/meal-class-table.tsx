import {MealClassTableProps} from './props';
import {Table} from './styles';
import {MealTableHeader} from '../../../6_entities/meals/ui/meal-table-header';
import {MealTableTextCell} from '../../../6_entities/meals/ui/meal-table-text-cell';

export function MealClassTable(props: MealClassTableProps) {
  return (
    <Table
      width={props.width}>
      <MealTableHeader
        title={'Класс'}
        height={'60px'}
        fontSize={'16px'}/>
      <MealTableTextCell text={'1А'}/>
      <MealTableTextCell text={'1А'}/>
      <MealTableTextCell text={'1А'}/>
      <MealTableTextCell text={'1А'}/>
      <MealTableTextCell text={'1А'}/>
      <MealTableHeader
        title={'Всего'}
        height={'40px'}
        fontSize={'14px'}/>
    </Table>
  );
}
