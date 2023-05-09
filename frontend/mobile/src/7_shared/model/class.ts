import {School} from "./school";
import {Teachers} from "./teachers";
import {Child} from "../../6_entities/child/model/child";

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