import styled from 'styled-components';
import {ButtonPrimaryShadowedStyles} from './props.ts';
import {DefaultStyles} from './config.ts';

export const ButtonContainer = styled(DefaultStyles)<ButtonPrimaryShadowedStyles>`
  background-color: ${props => props.$backgroundColor};
  border-radius: ${props => props.$borderRadius};
  color: ${props => props.$textColor};
  font-size: ${props => props.$fontSize};
  font-family: ${props => props.$fontFamily};
  padding-top: ${props => props.$paddingVertical};
  padding-bottom: ${props => props.$paddingVertical};
  padding-left: ${props => props.$paddingHorizontal};
  padding-right: ${props => props.$paddingHorizontal};
  width: 100%;
  border-width: 0;

  &:hover {
    background-color: #e57645;
    transition: 0.3s linear;
  }

  &:active {
    background-color: #d5551c;
    transition: 0.3s linear;
  }
`;
