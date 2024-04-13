import {MealtimesPatchBody} from '../../backend-types/nutrition/mealtime.ts';
import {Pupil} from './pupil.ts';

export enum Mealtime {
  breakfast = 'breakfast',
  dinner = 'dinner',
  snacks = 'snacks'
}

export type MealtimesUpdate = {
  pupilId: Pupil['id']
} & MealtimesPatchBody;
