import {Class} from "../../../7_shared/model/class";
import {CancelMealPeriods} from "../../../7_shared/model/cancelMealPeriods";

export type Child = {
    id: number,
    lastName: string,
    firstName: string,
    certificateBeforeDate: string,
    balance: number,
    breakfast: boolean,
    lunch: boolean,
    dinner: boolean,
    class: Class,
    cancelMealPeriods: CancelMealPeriods[]
}
