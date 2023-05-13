import {PropsWithChildren} from 'react';
import {PropsWithNavigation} from "../../../../7_shared/model/props-with-navigation";

export type ChildCardProps = {
    childPagePath: string,
    nameChild: string,
    schoolAdress: string,
    classNumberAndLetter: string,
    certificateBeforeDate: string,
} & PropsWithChildren & PropsWithNavigation;
