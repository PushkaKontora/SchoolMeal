import {DayComponentProps} from '../model/props';
import {DimensionValue, ViewStyle} from 'react-native';
import {MarkedDates} from 'react-native-calendars/src/types';
import {dateToISOWithoutTime} from '../../../../../lib/date';

export function isStartingDay(props: DayComponentProps) {
  return props.marking?.startingDay;
}

export function isEndingDay(props: DayComponentProps) {
  return props.marking?.endingDay;
}

export function isBorderDay(props: DayComponentProps) {
  return isStartingDay(props) || isEndingDay(props);
}

export function isMarkedDay(props: DayComponentProps) {
  return props.marking?.startingDay !== undefined &&
    props.marking?.endingDay !== undefined;
}

export function showAbsoluteBackground(props: DayComponentProps) {
  return isMarkedDay(props) &&
    !(props.marking?.startingDay &&
    props.marking?.endingDay);
}

export function selectAbsoluteBackgroundStyles(props: DayComponentProps): ViewStyle {
  let left: DimensionValue = '0%';
  if (isStartingDay(props)) {
    left = '50%';
  }

  let width: DimensionValue = '50%';
  if (!isBorderDay(props)) {
    width = '100%';
  }

  let backgroundColor = '#FFEEE8';
  if (!showAbsoluteBackground(props)) {
    backgroundColor = '#00000000';
  }

  return {
    left: left,
    width: width,
    backgroundColor: backgroundColor
  };
}

export function generatePeriod(startingDate: string, endingDate: string) {
  const result: MarkedDates = {};

  const date = new Date(startingDate);
  const endingDateObject = new Date(endingDate);
  let isoDate = dateToISOWithoutTime(date);

  while (date <= endingDateObject) {
    result[isoDate] = {
      startingDay: false,
      endingDay: false
    };

    date.setDate(date.getDate() + 1);
    isoDate = dateToISOWithoutTime(date);
  }

  result[startingDate].startingDay = true;
  result[endingDate].endingDay = true;

  return result;
}
