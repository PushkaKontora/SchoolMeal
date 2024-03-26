import {UUID} from './uuid.ts';

/**
 * @deprecated
 */
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
