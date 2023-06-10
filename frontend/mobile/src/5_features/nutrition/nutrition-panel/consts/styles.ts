import {StyleSheet} from 'react-native';

export const styles = StyleSheet.create({
  container: {
    marginTop: 28,
    width: '100%'
  },
  title: {
    fontWeight: '600',
    fontSize: 16
  },
  description: {
    fontWeight: '500',
    fontSize: 12,
    color: '#B1B1B1',
    marginTop: 4
  },
  calendar: {
    marginTop: 15
  },
  monthPicker: {
    width: '100%',
    alignItems: 'center',
    marginTop: 13
  },
  emojiContainer: {
    width: '100%'
  }
});

export const modalStyles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignContent: 'center'
  },
  title: {
    marginTop: 24,
    marginBottom: 32,
    marginHorizontal: 48,
    fontSize: 16,
    fontWeight: '500',
    textAlign: 'center'
  }
});
