import {getCoreRowModel, useReactTable} from '@tanstack/react-table';
import {ReactTableWrapper} from '../../../../../7_shared/lib/react-table-wrapper';
import {createColumns} from '../config/columns.tsx';
import {MealRequestMonitorTableProps} from '../model/props.ts';

export function MealRequestMonitorTable(props: MealRequestMonitorTableProps) {
  const table = useReactTable({
    data: props.data || [],
    getCoreRowModel: getCoreRowModel(),
    columns: createColumns(
      props.cells.CommonValueCell,
      props.cells.TotalValueBadgeCell,
      props.cells.FooterValueBadgeCell
    )
  });

  return (
    <ReactTableWrapper
      footerAtTop
      table={table}
      styles={{
        width: '100%'
      }}/>
  );
}
