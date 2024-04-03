import {MealtimeOut} from './mealtime.ts';

export enum ClassType {
  primary = 'primary',
  high = 'high'
}

export type GetPortionsParams = {
  class_type: ClassType,
  on_date: string
}

export type PortionsOut = {
  paid: number,
  preferential: number,
  total: number
}

export type MealtimePortionsOut = {
  [mealtime in MealtimeOut]: PortionsOut
}

export type SchoolClassWithPortionsOut = {
  id: string,
  number: number,
  literal: string,
  portions: MealtimePortionsOut
}

export type PortionsReportResponse = {
  schoolClasses: SchoolClassWithPortionsOut[],
  totals: MealtimePortionsOut
}
