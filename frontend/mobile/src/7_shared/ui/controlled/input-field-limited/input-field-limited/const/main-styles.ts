import {StyleSheet} from 'react-native';
import {InputStyle} from '../../../../fields/input-field';

export const createStyle = (props: InputStyle | undefined) => StyleSheet.create({
  internalField: {
    borderWidth: 0,
    width: '100%',
    backgroundColor: '#00000000',
    fontWeight: '500',
    fontSize: 12,
    textAlignVertical: 'top',
    paddingVertical: 0,
    paddingHorizontal: 0,
    color: props?.color || '#151515'
  },
  container: {
    width: props?.width || '100%',
    paddingVertical: props?.paddingVertical || 12,
    paddingHorizontal: props?.paddingHorizontal || 12,
    backgroundColor: props?.backgroundColor || '#00000000',
    borderRadius: props?.borderRadius || 10,
    borderColor: '#E9E9E9',
    borderWidth: props?.borderWidth || 1,
    flexDirection: 'column',
    gap: 10,
    alignItems: 'flex-end'
  },
  containerActive: {
    borderColor: props?.borderColor || '#FFC9B1'
  }
});

