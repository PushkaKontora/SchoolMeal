import {ClassType} from '../../../7_shared/model/class-type.ts';

export const CLASS_NAMES = ['1-4 классы', '5-11 классы'];

export const ClassTypesByIndex: {[index: number]: ClassType} = {
  0: ClassType.primary,
  1: ClassType.high
};
