import styled from 'styled-components';
import {MealTableValueCellStyles} from './props';
import {DEFAULT_STYLES} from './config';

export const Row = styled.tr<MealTableValueCellStyles>`
  display: flex;
  flex-direction: row;

  height: 40px;
  
  justify-content: space-around;
  align-items: center;

  border-bottom: 1px solid #F3F6F9;
  box-sizing: border-box;
  
  background-color: ${props => props.backgroundColor || DEFAULT_STYLES.backgroundColor};
  border-radius: ${props => props.borderRadius || DEFAULT_STYLES.borderRadius};
`;
