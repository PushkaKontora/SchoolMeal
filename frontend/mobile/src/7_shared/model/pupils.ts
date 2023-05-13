import {Parents} from "./parents";

export type Pupils ={
    id: number,
    lastName: string,
    firstName: string,
    certificateBefore: string,
    balance: number,
    breakfast: boolean,
    lunch: boolean,
    dinner: boolean,
    parents: Parents[],
}