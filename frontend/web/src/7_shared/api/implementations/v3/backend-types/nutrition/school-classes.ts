import {MealtimeOut} from './mealtime.ts';

export type GetSchoolClassesParams = {
  teacher_id: string
}

export type SchoolClassOut = {
  id: string,
  teacherId: string,
  number: number,
  literal: string,
  mealtimes: MealtimeOut[]
}

export type SchoolClassesResponse = SchoolClassOut[]
