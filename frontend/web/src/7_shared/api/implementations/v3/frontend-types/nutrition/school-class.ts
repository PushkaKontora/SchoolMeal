import {Mealtime} from './mealtime.ts';

export type SchoolClass = {
  id: string,
  teacherId: string,
  number: number,
  literal: string,
  mealtimes: Mealtime[]
}
