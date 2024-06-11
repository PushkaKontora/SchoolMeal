import styled from 'styled-components';
import {ButtonPrimaryStyles} from './props';
import {DEFAULT_STYLES} from './config';

export const ButtonContainer = styled.button<ButtonPrimaryStyles>`
  padding: ${DEFAULT_STYLES.padding};
  background-color: ${DEFAULT_STYLES.backgroundColor};
  color: ${DEFAULT_STYLES.color};
  font-size: ${props => props.fontSize || DEFAULT_STYLES.fontSize};
  border-radius: ${DEFAULT_STYLES.borderRadius};
  font-weight: ${DEFAULT_STYLES.fontWeight};
  font-family: ${DEFAULT_STYLES.fontFamily};

  width: 100%;
  border-width: 0;

  transition: 0.1s linear;

  &:hover {
    background-color: #e57645;
    cursor: pointer;
  }

  &:active {
    background-color: #d5551c;
  }
  
  &:disabled {
    opacity: 0.3;
  }
`;
