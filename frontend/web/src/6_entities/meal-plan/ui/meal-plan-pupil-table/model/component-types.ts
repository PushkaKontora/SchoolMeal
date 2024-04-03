import {ComponentType, CSSProperties} from 'react';
import {NutritionStatusView} from '../../../model/nutrition-status-view.ts';

export type IHeaderTextCell = ComponentType<{
  key: string,
  title: string,
  justifyContent?: CSSProperties['justifyContent'],
  width?: CSSProperties['width'],
  whiteSpace?: CSSProperties['whiteSpace']
}>;

export type IValueTextCell = ComponentType<{
  key: string,
  title: string,
  whiteSpace?: CSSProperties['whiteSpace']
}>;

export type IStatusCell = ComponentType<{
  key: string,
  status: NutritionStatusView,
  width?: CSSProperties['width'],
  whiteSpace?: CSSProperties['whiteSpace']
}>;

export type ISwitchCell = ComponentType<{
  key: string,
  toggled: boolean,
  disabled: boolean,
  onToggle: () => void
}>;
