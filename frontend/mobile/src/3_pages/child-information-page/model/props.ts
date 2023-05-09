import {PropsWithChildren} from 'react';
import {Child} from "../../../6_entities/child/model/child";

export type ChildInformationProps = {
    childInformation: Child
} & PropsWithChildren;
