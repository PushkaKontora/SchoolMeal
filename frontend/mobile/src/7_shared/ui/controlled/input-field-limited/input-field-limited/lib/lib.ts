import {createStyle} from '../const/main-styles';
import {StyleSheet} from 'react-native';

export function composeStyles(styles: ReturnType<typeof createStyle>) {
  return {
    default: styles.container,
    active: StyleSheet.compose(styles.container, styles.containerActive)
  };
}

export function applyViewStyle(viewStyles: ReturnType<typeof composeStyles>, focused: boolean) {
  return focused ? viewStyles.active : viewStyles.default;
}
