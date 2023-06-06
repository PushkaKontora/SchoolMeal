import {StyleSheet} from 'react-native';

export const styles = StyleSheet.create({
  container: {
    flexDirection: 'column',
    gap: 16,
    alignItems: 'center'
  }
});

export const monthPicker = StyleSheet.create({
  container: {
    flexDirection: 'row',
    gap: 4,
    alignItems: 'center'
  },
  monthName: {
    fontWeight: '600',
    fontSize: 14,
    width: 70,
    textAlign: 'center'
  }
});

export const datePicker = StyleSheet.create({
  container: {
    width: '100%',
    flexDirection: 'row',
    gap: 16,
    justifyContent: 'space-between',
    alignItems: 'center'
  }
});

export const dateButton = (color: string) => StyleSheet.create({
  container: {
    flexDirection: 'column',
    borderRadius: 10,
    justifyContent: 'space-around',
    alignItems: 'center',
    width: 36,
    height: 36,
    paddingVertical: 5.5
  },
  checked: {
    backgroundColor: color
  },
  textContainer: {
    lineHeight: 11,
    fontSize: 11,
    fontWeight: '500',
  },
  checkedText: {
    color: '#FFFFFF'
  },
  unchecked: {
    backgroundColor: '#F7F7F7',
    borderColor: '#E5E5E5',
    borderWidth: 1
  },
  uncheckedText: {
    color: '#2C2C2C'
  }
});
