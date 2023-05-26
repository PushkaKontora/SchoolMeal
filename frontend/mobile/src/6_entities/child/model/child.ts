import {Class} from '../../../7_shared/model/class';
import {CancelMealPeriods} from '../../../7_shared/model/cancelMealPeriods';

export type Child = {
    id: string,
    lastName: string,
    firstName: string,
    certificateBeforeDate: Date | null,
    balance: number,
    breakfast: boolean,
    lunch: boolean,
    dinner: boolean,
    schoolClass: Class,
    cancelMealPeriods: CancelMealPeriods[]
}
