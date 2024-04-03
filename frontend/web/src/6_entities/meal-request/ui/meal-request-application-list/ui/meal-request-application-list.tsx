import {MealRequestListProps} from '../model/props.ts';
import {getCoreRowModel, useReactTable} from '@tanstack/react-table';
import {createColumns} from '../config/columns.tsx';
import {ReactTableWrapper} from '../../../../../7_shared/lib/react-table-wrapper';

export function MealRequestApplicationList(props: MealRequestListProps) {
  const table = useReactTable({
    data: props.data || [],
    columns: createColumns(
      props.tableData,
      props.cells.mealPlanHeader,
      props.cells.cancelledBadge),
    getCoreRowModel: getCoreRowModel(),
    meta: {
      updateData: (rowIndex, columnId, value) => {
        props.updateData(rowIndex, columnId, value);
      }
    }
  });

  return (
    <ReactTableWrapper
      table={table}
      styles={{
        width: '100%'
      }}/>
  );
}
