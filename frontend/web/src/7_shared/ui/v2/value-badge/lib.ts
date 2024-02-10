import {ValueBadgeProps, ValueBadgeStyles} from './props.ts';

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
