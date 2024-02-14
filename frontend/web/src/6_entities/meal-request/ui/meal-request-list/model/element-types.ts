import {ComponentType} from 'react';

export type IMealPlanHeaderView = ComponentType<{
  key: string,
  title: string,
  price: number
}>

export type ICancelledNutritionView = ComponentType<{
  key: string,
  cancelled: boolean
}>
