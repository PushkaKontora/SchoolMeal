import {MealPlanPupilTableProps} from '../model/props.ts';
import {getCoreRowModel, useReactTable} from '@tanstack/react-table';
import {createColumns} from '../config/columns.tsx';
import {ReactTableWrapper} from '../../../../../7_shared/lib/react-table-wrapper';

export function MealPlanPupilTable(props: MealPlanPupilTableProps) {
  const table = useReactTable({
    data: props.data || [],
    columns: createColumns(
      props.tableData,
      props.cells
    ),
    getCoreRowModel: getCoreRowModel(),
    meta: {
      updateData: (rowIndex, columnId, value) => {
        props.updateData(rowIndex, columnId, value);
      }
    }
  });

  return (
    <ReactTableWrapper
      table={table}/>
  );
}
