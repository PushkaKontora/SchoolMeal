import {StyleSheet} from 'react-native';

export const createStyle = () => StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: '#F7F7F7',
    borderRadius: 10,
    gap: 8,
    marginBottom: 4,
    padding: 8,
    alignItems: 'center',
  },
  imageContainer: {
    height: 32,
    width: 32,
    borderRadius: 100,
  },
  image: {
    height: 32,
    width: 32,
    borderRadius: 100,
  },
  textContainer: {
    flexDirection: 'column',
    gap: 4,
  },
  textPart: {
    fontWeight: '500',
    fontSize: 12,
    lineHeight: 12
  },

  containerModal: {
    backgroundColor: '#FFFFFF',
    borderTopLeftRadius: 10,
    borderTopRightRadius: 10,
    marginTop: 'auto',
  },

});
