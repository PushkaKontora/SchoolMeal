import {PropsWithChildren} from 'react';
import {Child} from "../../../../../6_entities/child/model/child";

export type ChildPersonalInformationProps = {
    childInformation: Child,
} & PropsWithChildren;
