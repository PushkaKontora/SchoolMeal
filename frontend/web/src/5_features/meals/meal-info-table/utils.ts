import {MealCellData} from './types';

export function createTotalCell(cells: MealCellData[]) {
  return {
    paid: cells.reduce((acc, obj) => acc + obj.paid, 0),
    preferential: cells.reduce((acc, obj) => acc + obj.preferential, 0),
    sum: cells.reduce((acc, obj) => acc + obj.sum, 0)
  };
}
