import {Class} from './class-view';
import {Pupil} from './pupil-view';

export type Meal = {
  id: number,
  creatorId: number,
  mealId: number,
  createdAt: Date,
  date: string,
  schoolClass: Class,
  pupils: Pupil[]
}
