import {ValueBadgeProps, ValueBadgeStyles} from './props.ts';
import {showDash} from './const.ts';

export function applyShowDashProp(showDashProp: ValueBadgeProps['showDash']): (value: ValueBadgeProps['value']) => boolean {
  if (showDashProp === undefined || showDashProp == 'standard')
    return showDash;
  if (typeof showDashProp === 'boolean')
    return () => showDashProp;
  return showDashProp;
}

export function getStylesFromType(type: ValueBadgeProps['type'], ): ValueBadgeStyles {
  switch (type) {
  case 'positive':
    return {
      backgroundColor: '#EFFBF7',
      textColor: '#2FCB8F'
    };
  case 'negative':
    return {
      backgroundColor: '#fdefea',
      textColor: '#FF4F00'
    };
  }
  return {};
}
