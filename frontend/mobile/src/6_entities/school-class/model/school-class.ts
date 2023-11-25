import {School} from './school';
import {UUID} from '../../../7_shared/model/uuid';

export type SchoolClass = {
    id: UUID,
    school: School,
    number: number,
    literal: string,
}
