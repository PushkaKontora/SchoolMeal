import {ColumnDef, createColumnHelper} from '@tanstack/react-table';
import {MealRequestRowViewData} from '../model/meal-request-row-view-data.ts';
import {TextCell} from '../../../../../7_shared/ui/v2/table';
import {createSchoolClassName} from '../lib/create-school-class-name.ts';
import {IValueBadgeCellView} from '../model/value-badge-cell-view.ts';

export const columnHelper = createColumnHelper<MealRequestRowViewData>();

export const createColumns = (
  CommonValueCell: IValueBadgeCellView,
  TotalValueBadge: IValueBadgeCellView,
  FooterTotalValueBadge: IValueBadgeCellView
)
  : ColumnDef<MealRequestRowViewData, any>[] => [
  columnHelper.group({
    id: 'class-group',
    header: props => <TextCell
      header
      text={'Класс'}
      key={props.header.id}
      rowSpan={2}
      cellStyles={{
        width: '15%',
        whiteSpace: 'nowrap'
      }}/>,
    columns: [
      columnHelper.accessor(originalRow => createSchoolClassName(originalRow.schoolClass),{
        id: 'schoolClass',
        header: undefined,
        cell: props => <TextCell
          key={props.cell.id}
          text={props.getValue()}
          cellStyles={{
            whiteSpace: 'nowrap'
          }}/>
      }),
    ]
  }),
  columnHelper.group({
    id: 'breakfast',
    header: () => <TextCell
      header
      text={'Завтрак'}
      key={'breakfast'}
      columnSpan={3}
      cellStyles={{
        height: '36px'
      }}
      styles={{
        justifyContent: 'center'
      }}/>,
    columns: [
      columnHelper.accessor(originalRow => originalRow.breakfast.paid, {
        id: 'breakfast-paid',
        header: props => <TextCell
          header
          text={'Платно'}
          key={props.header.id}
          cellStyles={{
            height: '36px'
          }}
          styles={{
            justifyContent: 'center'
          }}/>,
        cell: props => <CommonValueCell
          key={props.cell.id}
          value={props.getValue()}/>
      }),
      columnHelper.accessor(originalRow => originalRow.breakfast.preferential, {
        id: 'breakfast-preferential',
        header: props => <TextCell
          header
          text={'Льготно'}
          key={props.header.id}
          cellStyles={{
            height: '36px'
          }}
          styles={{
            justifyContent: 'center'
          }}/>,
        cell: props => <CommonValueCell
          key={props.cell.id}
          value={props.getValue()}/>
      }),
      columnHelper.accessor(originalRow => originalRow.breakfast.total, {
        id: 'breakfast-total',
        header: props => <TextCell
          header
          text={'Всего'}
          key={props.header.id}
          cellStyles={{
            height: '36px'
          }}
          styles={{
            justifyContent: 'center'
          }}/>,
        cell: props => <TotalValueBadge
          key={props.cell.id}
          value={props.getValue()}/>
      }),
    ]
  }),
  columnHelper.group({
    id: 'dinner',
    header: () => <TextCell
      header
      text={'Обед'}
      key={'dinner'}
      columnSpan={3}
      cellStyles={{
        height: '36px'
      }}
      styles={{
        justifyContent: 'center'
      }}/>,
    columns: [
      columnHelper.accessor(originalRow => originalRow.dinner.paid, {
        id: 'dinner-paid',
        header: props => <TextCell
          header
          text={'Платно'}
          key={props.header.id}
          cellStyles={{
            height: '36px'
          }}
          styles={{
            justifyContent: 'center'
          }}/>,
        cell: props => <CommonValueCell
          key={props.cell.id}
          value={props.getValue()}/>
      }),
      columnHelper.accessor(originalRow => originalRow.dinner.preferential, {
        id: 'dinner-preferential',
        header: props => <TextCell
          header
          text={'Льготно'}
          key={props.header.id}
          cellStyles={{
            height: '36px'
          }}
          styles={{
            justifyContent: 'center'
          }}/>,
        cell: props => <CommonValueCell
          key={props.cell.id}
          value={props.getValue()}/>
      }),
      columnHelper.accessor(originalRow => originalRow.dinner.total, {
        id: 'dinner-total',
        header: props => <TextCell
          header
          text={'Всего'}
          key={props.header.id}
          cellStyles={{
            height: '36px'
          }}
          styles={{
            justifyContent: 'center'
          }}/>,
        cell: props => <TotalValueBadge
          key={props.cell.id}
          value={props.getValue()}/>
      }),
    ]
  }),
  columnHelper.group({
    id: 'snacks',
    header: () => <TextCell
      header
      text={'Полдник'}
      key={'snacks'}
      columnSpan={3}
      cellStyles={{
        height: '36px'
      }}
      styles={{
        justifyContent: 'center'
      }}/>,
    columns: [
      columnHelper.accessor(originalRow => originalRow.snacks.paid, {
        id: 'snacks-paid',
        header: props => <TextCell
          header
          text={'Платно'}
          key={props.header.id}
          cellStyles={{
            height: '36px'
          }}
          styles={{
            justifyContent: 'center'
          }}/>,
        cell: props => <CommonValueCell
          key={props.cell.id}
          value={props.getValue()}/>
      }),
      columnHelper.accessor(originalRow => originalRow.snacks.preferential, {
        id: 'snacks-preferential',
        header: props => <TextCell
          header
          text={'Льготно'}
          key={props.header.id}
          cellStyles={{
            height: '36px'
          }}
          styles={{
            justifyContent: 'center'
          }}/>,
        cell: props => <CommonValueCell
          key={props.cell.id}
          value={props.getValue()}/>
      }),
      columnHelper.accessor(originalRow => originalRow.snacks.total, {
        id: 'snacks-total',
        header: props => <TextCell
          header
          text={'Всего'}
          key={props.header.id}
          cellStyles={{
            height: '36px'
          }}
          styles={{
            justifyContent: 'center'
          }}/>,
        cell: props => <TotalValueBadge
          key={props.cell.id}
          value={props.getValue()}/>
      }),
    ]
  }),
];
