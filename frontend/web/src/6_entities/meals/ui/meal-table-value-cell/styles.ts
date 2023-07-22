import styled from 'styled-components';
import {MealTableValueCellStyles} from './props';
import {DEFAULT_STYLES} from './config';

export const Row = styled.tr<MealTableValueCellStyles>`
  display: flex;
  flex-direction: row;

  height: 45px;
  
  justify-content: space-around;
  align-items: center;
  
  background-color: ${props => props.backgroundColor || DEFAULT_STYLES.backgroundColor};
  border-radius: ${props => props.borderRadius || DEFAULT_STYLES.borderRadius};
`;
