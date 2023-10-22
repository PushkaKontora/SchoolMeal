import {StyleSheet} from 'react-native';
import {ChildCardHeaderProps} from './props';

export const createStyle = (props: ChildCardHeaderProps) => StyleSheet.create({
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
