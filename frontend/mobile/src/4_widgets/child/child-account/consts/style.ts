import {StyleSheet} from 'react-native';

export const createStyle = () => StyleSheet.create({
  container: {
    flexDirection: 'row',
    gap: 8,
    alignItems: 'center',

    backgroundColor: '#2C2C2C',
    borderRadius: 10,
    paddingVertical: 12,
    paddingHorizontal: 12,
  },
  containerContent: {
    flexDirection: 'row',
    gap: 4,
    alignItems: 'center',
  },
  content: {
    color: '#FFFFFF',
    fontSize: 12,
    lineHeight: 14,
    fontWeight: '700',
  },
  contentRuble: {
    color: '#FFFFFF',
    fontSize: 12,
    lineHeight: 14,
    fontWeight: '300',
  },
  containerButton: {
    marginLeft: 'auto',
  }
});
