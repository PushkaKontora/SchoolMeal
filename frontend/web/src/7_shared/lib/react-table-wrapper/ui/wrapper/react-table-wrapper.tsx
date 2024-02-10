import {ReactTableWrapperProps} from './props.ts';
import {flexRender} from '@tanstack/react-table';
import {TableContainer} from './styles.ts';

export function ReactTableWrapper<T>({table, ...props}: ReactTableWrapperProps<T>) {
  return (
    <TableContainer
      $width={props.styles?.width}>
      <thead>
        {
          table.getHeaderGroups().map(group => (
            <tr
              key={group.id}>
              {
                group.headers.map(header => flexRender(
                  header.column.columnDef.header,
                  header.getContext()
                ))
              }
            </tr>
          ))
        }
      </thead>
      <tbody>
        {
          table.getRowModel().rows.map(row => (
            <tr key={row.id}>
              {
                row.getVisibleCells().map(cell => flexRender(
                  cell.column.columnDef.cell,
                  cell.getContext()
                ))
              }
            </tr>
          ))
        }
      </tbody>
    </TableContainer>
  );
}
