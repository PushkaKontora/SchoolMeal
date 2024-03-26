import {Food} from './food.ts';

/**
 * @deprecated
 */
export type MealtimeInfo = {
  foods: Food[],
  cost: string
}

/**
 * @deprecated
 */
export type Menu = {
  id: string,
  onDate: string,
  breakfast: MealtimeInfo,
  dinner: MealtimeInfo,
  snacks: MealtimeInfo
}
