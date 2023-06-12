import styled from 'styled-components';
import {MealClassTableStyles} from './props';

export const Table = styled.table<MealClassTableStyles>`
  width: ${props => props.width};
  border-collapse: collapse;
`;
