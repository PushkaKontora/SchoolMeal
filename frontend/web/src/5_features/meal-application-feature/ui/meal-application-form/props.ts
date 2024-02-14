import {HeaderViewData, MealRequestRowViewData} from '../../../../6_entities/meal-request';
import {MealRequestStatus} from '../../../../7_shared/model/meal-request-status.ts';
import {CSSProperties} from 'react';

export type TableStyles = {
  height?: CSSProperties['height']
}

export type MealApplicationFormProps = {
  data?: MealRequestRowViewData[],
  updateData: (rowIndex: number, columnId: string, value: unknown) => void,
  headerViewData: HeaderViewData,
  status: MealRequestStatus,
  buttonTitles: {
    [key in MealRequestStatus]: string
  },
  onSend: () => void,
  tableStyles?: TableStyles
}
