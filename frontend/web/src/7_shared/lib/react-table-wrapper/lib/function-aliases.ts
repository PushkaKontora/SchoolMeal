import {CellContext} from '@tanstack/react-table';

export function updateCellData(props: CellContext<any, any>, newValue: unknown) {
  props.table.options.meta?.updateData(
    props.row.index,
    props.column.id,
    newValue);
}
