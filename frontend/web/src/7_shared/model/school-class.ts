import {UUID} from './uuid.ts';

export type SchoolClass = {
  id: UUID,
  initials: {
    literal: string,
    number: number
  },
  breakfast: boolean,
  dinner: boolean,
  snacks: boolean
}
