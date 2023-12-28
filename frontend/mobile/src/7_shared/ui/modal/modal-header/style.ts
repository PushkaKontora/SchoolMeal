import {StyleSheet} from 'react-native';

export const createStyle = () => StyleSheet.create({
  headerContent:{
    flexDirection: 'row',
    alignItems: 'center',
    borderBottomColor: '#F3F3F3',
    borderBottomWidth: 0.7,
    height: 48
  },
  headerTitle: {
    fontWeight: '700',
    fontSize: 16,
    flex: 1,
    textAlign: 'center',
    color: '#212121',
  },
  image: {
    position: 'absolute',
    top: 16,
    right: 24
  }
});
