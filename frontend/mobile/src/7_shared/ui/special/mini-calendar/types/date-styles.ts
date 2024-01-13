import {StyleSheet} from 'react-native';
import {StandardDateProperties} from './date-properties';
import NamedStyles = StyleSheet.NamedStyles;

export type DateButtonStyleNames = {
  container: any,
  dayNumber: any,
  dayName: any
};

export type DateButtonStyles = {
  [property in keyof StandardDateProperties]: ReturnType<typeof StyleSheet.create<NamedStyles<DateButtonStyleNames>>>
};

/*
{
  [index: string]: ReturnType<typeof StyleSheet.create<NamedStyles<StandardDateProperties>>>
}
 */
