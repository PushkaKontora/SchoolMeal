import {School} from './school';
import {Teachers} from '../../../7_shared/model/teachers';

export type Class   = {
    id: number,
    number: number,
    letter: string,
    hasBreakfast: boolean,
    hasLunch: boolean,
    hasDinner: boolean,
    school: School,
    teachers: Teachers[],
}
