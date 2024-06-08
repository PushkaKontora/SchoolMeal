import styled from 'styled-components';
import {SidebarIconedButtonContainer, SidebarIconedButtonText} from '../iconed-button/styles.ts';

export const ButtonContainer =
  styled(SidebarIconedButtonContainer)`
    background-color: #333333;
    margin-top: 8px;
    
    flex-direction: row-reverse;
    
    cursor: pointer;
  `;

export const ButtonText
  = styled(SidebarIconedButtonText)`
    color: #FFFFFF;
  `;
