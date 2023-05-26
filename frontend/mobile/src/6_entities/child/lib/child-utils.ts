import {Child} from '../model/child';

export function getFullName(child: Child) {
  return child.firstName + ' ' + child.lastName;
}
