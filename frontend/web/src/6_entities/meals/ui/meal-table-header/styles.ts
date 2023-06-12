import styled from 'styled-components';
import {MealTableHeaderStyles} from './props';

export const Title = styled.tr<MealTableHeaderStyles>`
  display: flex;
  
  width: 100%;
  height: ${props => props.height};

  background-color: #F3F6F9;
  
  border-radius: 6px 0 0 6px;

  letter-spacing: 0.03em;
  
  td {
    align-self: center;
    
    font-family: 'Ubuntu';
    font-size: ${props => props.fontSize};
    font-weight: 800;

    color: #464E5F;

    vertical-align: middle;
    
    padding-left: 32px;
  }
`;