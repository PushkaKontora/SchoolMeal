import {HeaderViewData, MealRequestRowViewData} from '../../../../6_entities/meal-request';
import {MealRequestStatus} from '../../../../7_shared/model/meal-request-status.ts';
import {CSSProperties} from 'react';
import {TableViewData} from '../../../../6_entities/meal-request/ui/meal-request-list/model/table-view-data.ts';

export type TableStyles = {
  height?: CSSProperties['height']
}

export type MealApplicationFormProps = {
  data?: MealRequestRowViewData[],
  updateData: (rowIndex: number, columnId: string, value: unknown) => void,
  tableData: TableViewData,
  headerViewData: HeaderViewData,
  status: MealRequestStatus,
  buttonTitles: {
    [key in MealRequestStatus]: string
  },
  onCancel: () => void,
  onSend: () => void,
  tableStyles?: TableStyles
}
