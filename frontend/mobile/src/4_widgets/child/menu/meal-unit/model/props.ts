import {PropsWithChildren} from "react";
import {Portions} from "../../../../../7_shared/model/portions";

export type MealUnitProps = {
    title: string,
    sum: string,
    portions: Portions[],
} & PropsWithChildren;
