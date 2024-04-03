import {Mealtime} from './mealtime.ts';

export type GetSchoolClassesParams = {
  teacherId: string
}

export type SchoolClass = {
  id: string,
  teacherId: string,
  number: number,
  literal: string,
  mealtimes: Mealtime[]
}
