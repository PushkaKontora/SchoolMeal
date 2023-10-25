import {StyleSheet} from 'react-native';

export const createStyle = () => StyleSheet.create({
  headerContent: {
    flexDirection: 'row',

    borderBottomColor: '#F3F3F3',
    borderBottomWidth: 0.7,
  },
  headerTitle: {
    fontWeight: '700',
    fontSize: 16,
    lineHeight: 18,

    color: '#212121',
  },
  imageArrow: {
    marginLeft: 'auto',
    paddingLeft: 10,
  }
});
