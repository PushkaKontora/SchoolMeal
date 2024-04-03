import {MealRequestRowViewData} from '../../../../6_entities/meal-request';
import {CSSProperties} from 'react';
import {TableViewData} from '../../../../6_entities/meal-request';
import {MealApplicationFormStatus} from '../../../../6_entities/meal-request/model/meal-application-form-status.ts';

export type TableStyles = {
  height?: CSSProperties['height']
}

export type MealApplicationFormProps = {
  data?: MealRequestRowViewData[],
  updateData: (rowIndex: number, columnId: string, value: unknown) => void,
  tableData: TableViewData,
  status: MealApplicationFormStatus,
  buttonTitles: {
    [key in MealApplicationFormStatus]: string
  },
  onCancel: () => void,
  onSend: () => void,
  tableStyles?: TableStyles
}
