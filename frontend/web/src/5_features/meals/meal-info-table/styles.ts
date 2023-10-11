import styled from 'styled-components';
import {MealInfoTableStyles} from './props';

export const Table = styled.table<MealInfoTableStyles>`
  width: ${props => props.width};
  border-collapse: collapse;
  
  padding: 35px 0;
`;
