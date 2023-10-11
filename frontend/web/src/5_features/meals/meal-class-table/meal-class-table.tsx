import {MealClassTableProps} from './props';
import {Table} from './styles';
import {MealTableHeader} from '../../../6_entities/meals/ui/meal-table-header';
import {MealTableTextCell} from '../../../6_entities/meals/ui/meal-table-text-cell';
import {TITLE, TOTAL} from './config';

export function MealClassTable(props: MealClassTableProps) {
  return (
    <Table
      width={props.width}>
      <tbody>
        <MealTableHeader
          title={TITLE}
          height={'60px'}
          fontSize={'16px'}/>

        {
          props.classNames.map((item, idx) => (
            <MealTableTextCell key={idx} text={item}/>
          ))
        }

        <MealTableHeader
          title={TOTAL}
          height={'40px'}
          fontSize={'14px'}/>
      </tbody>
    </Table>
  );
}
