import {PropsWithChildren} from "react";
import {Meals} from "../../../../../7_shared/model/meals";

export type MenuProps = {
    meals: Meals,
} & PropsWithChildren;
