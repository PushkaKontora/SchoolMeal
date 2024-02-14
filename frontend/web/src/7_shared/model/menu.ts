import {Food} from './food.ts';

export type MealtimeInfo = {
  foods: Food[],
  cost: string
}

export type Menu = {
  id: string,
  onDate: string,
  breakfast: MealtimeInfo,
  dinner: MealtimeInfo,
  snacks: MealtimeInfo
}
