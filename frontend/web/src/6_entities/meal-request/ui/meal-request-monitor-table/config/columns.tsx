import {ColumnDef, createColumnHelper} from '@tanstack/react-table';
import {MealRequestRowViewData} from '../model/meal-request-row-view-data.ts';
import {TextCell} from '../../../../../7_shared/ui/v2/table';
import {createSchoolClassName} from '../lib/create-school-class-name.ts';
import {IValueBadgeCellView} from '../model/value-badge-cell-view.ts';

export const columnHelper = createColumnHelper<MealRequestRowViewData>();

export const createColumns = (
  CommonValueCell: IValueBadgeCellView,
  TotalValueBadge: IValueBadgeCellView,
  /* eslint-disable @typescript-eslint/no-unused-vars */
  // @ts-expect-error May be useful later
  FooterTotalValueBadge: IValueBadgeCellView
)
  : ColumnDef<MealRequestRowViewData, any>[] => [
  columnHelper.group({
    id: 'class-group',
    header: props => <TextCell
      cellProps={{
        key: props.header.id,
        header: true,
        rowSpan: 2,
        cellStyles: {
          width: '15%',
          whiteSpace: 'nowrap'
        }
      }}
      text={'Класс'}
    />,
    columns: [
      columnHelper.accessor(originalRow => createSchoolClassName(originalRow.schoolClass),{
        id: 'schoolClass',
        header: undefined,
        cell: props => <TextCell
          cellProps={{
            key: props.cell.id,
            cellStyles: {
              whiteSpace: 'nowrap'
            }
          }}
          text={props.getValue()}
        />
      }),
    ]
  }),
  columnHelper.group({
    id: 'breakfast',
    header: () => <TextCell
      cellProps={{
        header: true,
        key: 'breakfast',
        columnSpan: 3,
        cellStyles: {
          height: '36px'
        }
      }}
      text={'Завтрак'}
      styles={{
        justifyContent: 'center'
      }}/>,
    columns: [
      columnHelper.accessor(originalRow => originalRow.breakfast.paid, {
        id: 'breakfast-paid',
        header: props => <TextCell
          cellProps={{
            header: true,
            key: props.header.id,
            cellStyles: {
              height: '36px'
            }
          }}
          text={'Платно'}
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
          cellProps={{
            header: true,
            key: props.header.id,
            cellStyles: {
              height: '36px'
            }
          }}
          text={'Льготно'}
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
          cellProps={{
            header: true,
            key: props.header.id,
            cellStyles: {
              height: '36px'
            }
          }}
          text={'Всего'}
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
      cellProps={{
        header: true,
        key: 'dinner',
        columnSpan: 3,
        cellStyles: {
          height: '36px'
        }
      }}
      text={'Обед'}
      styles={{
        justifyContent: 'center'
      }}/>,
    columns: [
      columnHelper.accessor(originalRow => originalRow.dinner.paid, {
        id: 'dinner-paid',
        header: props => <TextCell
          cellProps={{
            header: true,
            key: props.header.id,
            cellStyles: {
              height: '36px'
            }
          }}
          text={'Платно'}
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
          cellProps={{
            header: true,
            key: props.header.id,
            cellStyles: {
              height: '36px'
            }
          }}
          text={'Льготно'}
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
          cellProps={{
            header: true,
            key: props.header.id,
            cellStyles: {
              height: '36px'
            }
          }}
          text={'Всего'}
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
      cellProps={{
        header: true,
        key: 'snacks',
        columnSpan: 3,
        cellStyles: {
          height: '36px'
        }
      }}
      text={'Полдник'}
      styles={{
        justifyContent: 'center'
      }}/>,
    columns: [
      columnHelper.accessor(originalRow => originalRow.snacks.paid, {
        id: 'snacks-paid',
        header: props => <TextCell
          cellProps={{
            header: true,
            key: props.header.id,
            cellStyles: {
              height: '36px'
            }
          }}
          text={'Платно'}
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
          cellProps={{
            header: true,
            key: props.header.id,
            cellStyles: {
              height: '36px'
            }
          }}
          text={'Льготно'}
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
          cellProps={{
            header: true,
            key: props.header.id,
            cellStyles: {
              height: '36px'
            }
          }}
          text={'Всего'}
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
