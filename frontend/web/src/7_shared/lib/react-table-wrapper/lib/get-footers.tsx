import {flexRender, Table} from '@tanstack/react-table';

export function getFooters<T>(table: Table<T>) {
  return (
    table.getFooterGroups().map(group => (
      <tr key={group.id}>
        {
          group.headers.map(header => flexRender(
            header.column.columnDef.footer,
            header.getContext()
          ))
        }
      </tr>
    ))
  );
}
