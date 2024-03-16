import {ValueBadgeStyles} from '../../../../7_shared/ui/v2/value-badge/props.ts';

export type StyleTypes = 'totalInFooter' | 'total'

export const Styles: {[index in StyleTypes]: ValueBadgeStyles} = {
  totalInFooter: {
    backgroundColor: '#E9632C',
    textColor: '#FFFFFF'
  },
  total: {
    backgroundColor: '#2C2C2C',
    textColor: '#FFFFFF'
  }
};
