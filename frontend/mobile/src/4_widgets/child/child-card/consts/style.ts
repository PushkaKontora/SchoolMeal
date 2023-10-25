import {StyleSheet} from 'react-native';

export const createStyle = () => StyleSheet.create({
  container: {
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    marginTop: 8,
    // marginHorizontal: 16,
  },
  tagContainer: {
    flexDirection: 'column',
    gap: 4,
  },
  titles: {
    flexDirection: 'column',
    gap: 8,
    alignItems: 'center',
    marginBottom: 24
  },
  header: {
    fontWeight: '600',
    fontSize: 28
  },
  subHeader: {
    fontWeight: '400',
    fontSize: 14
  },
  content: {
    flexDirection: 'row',
    gap: 16,

    marginHorizontal: 16,
    marginVertical: 16,
  },
  statusMeal: {
    marginTop: 'auto',
    marginLeft: 'auto',

    fontWeight: '500',
    fontSize: 14,
    lineHeight: 16,
  },
  greyText: {
    fontWeight: '500',
    fontSize: 14,
    lineHeight: 16,
    color: '#909090',
  },
  blueText: {
    fontWeight: '500',
    fontSize: 14,
    lineHeight: 16,
    color: '#4941C4',
  },
  greenText: {
    fontWeight: '500',
    fontSize: 14,
    lineHeight: 16,
    color: '#51B078',
  }
});
