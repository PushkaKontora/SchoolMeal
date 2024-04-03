import {Mealtime} from './mealtime.ts';


export enum ClassType {
  primary = 'primary',
  high = 'high'
}

export type GetPortionsParams = {
  classType: ClassType,
  date: Date
}

export type Portions = {
  paid: number,
  preferential: number,
  total: number
}

export type MealtimePortions = {
  [mealtime in Mealtime]?: Portions
}

export type SchoolClassWithPortions = {
  id: string,
  number: number,
  literal: string,
  portions: MealtimePortions
}

export type PortionsReport = {
  schoolClasses: SchoolClassWithPortions[],
  totals: MealtimePortions
}
