import {ColumnDef, createColumnHelper} from '@tanstack/react-table';
import {TableRowViewData, TableViewData} from '../model/view-data.ts';
import {getFullName} from '../../../../user';
import {IHeaderTextCell, IStatusCell, ISwitchCell, IValueTextCell} from '../model/component-types.ts';
import {updateCellData} from '../../../../../7_shared/lib/react-table-wrapper';
import {toNutritionStatusView} from '../lib/nutrition-status-view.ts';

export const columnHelper = createColumnHelper<TableRowViewData>();

export const createColumns = (
  tableData: TableViewData,
  components: {
    HeaderTextCell: IHeaderTextCell,
    ValueTextCell: IValueTextCell,
    StatusCell: IStatusCell,
    SwitchCell: ISwitchCell
  }
) : ColumnDef<TableRowViewData, any>[] => [
  columnHelper.accessor(originalRow => getFullName(originalRow), {
    id: 'fullName',
    header: props => <components.HeaderTextCell
      key={props.header.id}
      title={'ФИО'}
      width={'1%'}
      whiteSpace={'nowrap'}
    />,
    cell: props => <components.ValueTextCell
      key={props.cell.id}
      title={props.getValue()}
      whiteSpace={'nowrap'}
    />
  }),
  columnHelper.accessor(originalRow => toNutritionStatusView(originalRow), {
    id: 'status',
    header: props => <components.HeaderTextCell
      key={props.header.id}
      title={'Статус'}
    />,
    cell: props => <components.StatusCell
      key={props.cell.id}
      width={'150px'}
      whiteSpace={'nowrap'}
      status={props.getValue()}
    />
  }),
  columnHelper.accessor('breakfast', {
    id: 'breakfast',
    header: props => <components.HeaderTextCell
      key={props.header.id}
      title={'Завтрак'}
      justifyContent={'center'}
    />,
    cell: props => <components.SwitchCell
      key={props.cell.id}
      disabled={!tableData.hasBreakfast}
      toggled={tableData.hasBreakfast && props.getValue()}
      onToggle={() => updateCellData(props, !props.getValue())}
    />
  }),
  columnHelper.accessor('dinner', {
    id: 'dinner',
    header: props => <components.HeaderTextCell
      key={props.header.id}
      title={'Обед'}
      justifyContent={'center'}
    />,
    cell: props => <components.SwitchCell
      key={props.cell.id}
      disabled={!tableData.hasDinner}
      toggled={tableData.hasDinner && props.getValue()}
      onToggle={() => updateCellData(props, !props.getValue())}
    />
  }),
  columnHelper.accessor('snacks', {
    id: 'snacks',
    header: props => <components.HeaderTextCell
      key={props.header.id}
      title={'Полдник'}
      justifyContent={'center'}
    />,
    cell: props => <components.SwitchCell
      key={props.cell.id}
      disabled={!tableData.hasSnacks}
      toggled={tableData.hasSnacks && props.getValue()}
      onToggle={() => updateCellData(props, !props.getValue())}
    />
  })
];
