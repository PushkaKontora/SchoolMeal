import {MealRequestRowViewData} from './meal-request-row-view-data.ts';
import {IValueBadgeCellView} from './value-badge-cell-view.ts';


export type MealRequestMonitorTableProps = {
  data?: MealRequestRowViewData[],
  cells: {
    CommonValueCell: IValueBadgeCellView,
    TotalValueBadgeCell: IValueBadgeCellView,
    FooterValueBadgeCell: IValueBadgeCellView
  },
}
