import {StyleSheet} from 'react-native';

export const createStyle = () => StyleSheet.create({
  container: {
    flex: 1,
    marginHorizontal: 16,
    marginTop: 8,
  },
  inputField: {
    backgroundColor: '#FFFFFF',
    borderRadius: 0,
    borderColor: '#E9E9E9',
    borderWidth: 1,
    color: '#212121',
  },
  content: {
    paddingHorizontal: 12,
    paddingBottom: 16,
    width: '100%',
  },
  contentTitle: {
    marginBottom: 8,
    fontWeight: '500',
    fontSize: 14,
    lineHeight: 16,
    color: '#212121'
  },
});
