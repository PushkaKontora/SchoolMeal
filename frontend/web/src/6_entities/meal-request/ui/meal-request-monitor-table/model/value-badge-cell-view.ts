import {ComponentType} from 'react';

export type IValueBadgeCellView = ComponentType<{
  key: string,
  value: string | undefined
}>
