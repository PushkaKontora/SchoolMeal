import {PropsWithChildren} from 'react';
import {Child} from "../../../../../6_entities/child/model/child";
import {PropsWithNavigation} from "../../../../../7_shared/model/props-with-navigation";

export type ChildPersonalInformationProps = {
    childInformation: Child,
} & PropsWithChildren & PropsWithNavigation;
