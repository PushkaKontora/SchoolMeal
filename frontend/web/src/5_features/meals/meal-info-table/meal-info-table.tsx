import {MealInfoTableProps} from './props';
import {Table} from './styles';
import {MealThreeColumnHeader} from '../../../6_entities/meals/ui/meal-three-column-header';
import {MealTableValueCell} from '../../../6_entities/meals/ui/meal-table-value-cell/meal-table-value-cell';
import {FOOTER_ROW_STYLES} from './config';
import {createTotalCell} from './utils';
import {useEffect, useState} from 'react';
import {MealCellData} from './types';

export function MealInfoTable(props: MealInfoTableProps) {
  const [cells, setCells] = useState<MealCellData[]>(props.data);
  const [totalCell, setTotalCell] = useState<MealCellData>(createTotalCell(props.data));

  useEffect(() => {
    setCells(props.data);
    setTotalCell(createTotalCell(props.data));
  }, [props.data]);

  return (
    <Table
      width={props.width}>
      <tbody>
        <MealThreeColumnHeader
          mealName={props.title}/>

        {
          cells.map((item, idx) => {
            return (
              <MealTableValueCell
                key={idx}
                paid={item.paid.toString()}
                preferential={item.preferential.toString()}
                total={item.sum.toString()}/>
            );
          })
        }

        <MealTableValueCell
          backgroundColor={FOOTER_ROW_STYLES.backgroundColor}
          paid={totalCell.paid.toString()}
          preferential={totalCell.preferential.toString()}
          total={totalCell.sum.toString()}/>
      </tbody>
    </Table>
  );
}
