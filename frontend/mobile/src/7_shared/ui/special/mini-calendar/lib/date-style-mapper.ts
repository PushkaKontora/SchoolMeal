import {StandardDateProperties} from '../types/date-properties';

export const standartStyleMapper = (properties: StandardDateProperties):keyof StandardDateProperties  => {
  if (properties.selected) {
    return 'selected';
  }
  if (properties.cancelled) {
    return 'cancelled';
  }
  return 'default';
};
