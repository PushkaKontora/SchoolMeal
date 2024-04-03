import {TableRowViewData, TableViewData} from './view-data.ts';
import {IHeaderTextCell, IStatusCell, ISwitchCell, IValueTextCell} from './component-types.ts';

export type MealPlanPupilTableProps = {
  data?: TableRowViewData[],
  tableData: TableViewData,
  updateData: (rowIndex: number, columnKey: string, value: unknown) => void,
  cells: {
    HeaderTextCell: IHeaderTextCell,
    ValueTextCell: IValueTextCell,
    StatusCell: IStatusCell,
    SwitchCell: ISwitchCell
  }
}
