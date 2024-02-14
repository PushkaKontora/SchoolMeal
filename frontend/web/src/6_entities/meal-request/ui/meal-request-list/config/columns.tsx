import {ColumnDef, createColumnHelper} from '@tanstack/react-table';
import {MealRequestRowViewData} from '../model/meal-request-row-view-data.ts';
import {getFullName, getTotalCost} from '../lib/mappers.ts';
import {AbstractCell, TextCell} from '../../../../../7_shared/ui/v2/table';
import {ValueBadgeCell} from '../../../../../7_shared/ui/v2/table';
import {HeaderViewData} from '../model/header-view-data.ts';
import {CheckboxCell} from '../../../../../7_shared/ui/v2/table';
import {setBalanceValueBadgeType} from '../lib/cell-utils.ts';
import {ICancelledNutritionView, IMealPlanHeaderView} from '../model/element-types.ts';
import {updateCellData} from '../../../../../7_shared/lib/react-table-wrapper';

export const columnHelper = createColumnHelper<MealRequestRowViewData>();

export const createColumns = (
  headerView: HeaderViewData,
  MealPlanHeader: IMealPlanHeaderView,
  CancelledBadge: ICancelledNutritionView
)
  : ColumnDef<MealRequestRowViewData, any>[] => [
  columnHelper.accessor(originalRow => getFullName(originalRow), {
    id: 'fullName',
    header: props => <TextCell
      header
      text={'ФИО'}
      key={props.header.id}
      cellStyles={{
        width: '1%',
        whiteSpace: 'nowrap'
      }}
    />,
    cell: props => <TextCell
      key={props.cell.id}
      text={props.getValue()}
      cellStyles={{
        whiteSpace: 'nowrap'
      }}/>
  }),
  columnHelper.accessor('cancelledMeal', {
    header: props => (
      <AbstractCell
        key={props.header.id}
        header/>
    ),
    cell: props => (
      <CancelledBadge
        key={props.cell.id}
        cancelled={props.cell.getValue()}/>
    )
  }),
  columnHelper.accessor('balance', {
    header: props => (
      <TextCell
        key={props.header.id}
        header
        cellStyles={{
          width: '10%'
        }}
        styles={{
          padding: '0px 28px'
        }}
        text={'Остаток'}/>
    ),
    cell: props => (
      <ValueBadgeCell
        key={props.cell.id}
        styles={{
          padding: '0px 28px'
        }}
        badgeProps={{
          value: props.getValue().toString(),
          type: setBalanceValueBadgeType(props.getValue())
        }}/>
    )
  }),
  columnHelper.accessor('breakfast', {
    header: props => <MealPlanHeader
      key={props.header.id}
      title={'Завтрак'}
      price={headerView.prices.breakfast}/>,
    cell: props => <CheckboxCell
      key={props.cell.id}
      disabled={false}
      checked={props.getValue()}
      onChange={() => updateCellData(props, !props.getValue())}/>
  }),
  columnHelper.accessor('dinner', {
    header: props => <MealPlanHeader
      key={props.header.id}
      title={'Обед'}
      price={headerView.prices.dinner}/>,
    cell: props => <CheckboxCell
      key={props.cell.id}
      disabled={false}
      checked={props.getValue()}
      onChange={() => updateCellData(props, !props.getValue())}/>
  }),
  columnHelper.accessor('snacks', {
    header: props => <MealPlanHeader
      key={props.header.id}
      title={'Полдник'}
      price={headerView.prices.snacks}/>,
    cell: props => <CheckboxCell
      key={props.cell.id}
      disabled={false}
      checked={props.getValue()}
      onChange={() => updateCellData(props, !props.getValue())}/>
  }),
  columnHelper.accessor(originalRow => getTotalCost(originalRow, headerView), {
    id: 'totalCost',
    header: props => (
      <TextCell
        key={props.header.id}
        header
        text={'ИТОГО'}
        cellStyles={{
          width: '15%'
        }}
        styles={{
          justifyContent: 'flex-end',
          padding: '0px 36px 0 28px'
        }}
      />
    ),
    cell: props => (
      <ValueBadgeCell
        key={props.cell.id}
        badgeProps={{
          value: props.getValue()
        }}
        styles={{
          justifyContent: 'flex-end',
          padding: '0px 28px'
        }}/>
    )
  })
];
