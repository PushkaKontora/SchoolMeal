import {dateButton} from './styles';
import {StyleSheet} from 'react-native';

export function createContainerStyle(selectionColor: string, checked: boolean) {
  const dateButtonStyle = dateButton(selectionColor);
  const style = checked ? dateButtonStyle.checked : dateButtonStyle.unchecked;

  return StyleSheet.compose(dateButtonStyle.container, style);
}

export function createTextStyle(selectionColor: string, checked: boolean) {
  const dateButtonStyle = dateButton(selectionColor);
  const style = checked ? dateButtonStyle.checkedText : dateButtonStyle.uncheckedText;

  return StyleSheet.compose(dateButtonStyle.textContainer, style);
}
