import {SchoolClass} from '../../../7_shared/api/implementations/v3/frontend-types/nutrition/school-class.ts';

export function createClassNames(classes?: SchoolClass[]) {
  if (!classes) {
    return [];
  }

  return classes?.map(classObject =>
    `${classObject.number}${classObject.literal}`);
}

