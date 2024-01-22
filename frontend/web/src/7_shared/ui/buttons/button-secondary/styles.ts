import styled from 'styled-components';
import {ButtonSecondaryStyles} from './props';
import {DEFAULT_STYLES} from './config';

export const ButtonContainer = styled.button<ButtonSecondaryStyles>`
  padding: ${DEFAULT_STYLES.padding};
  background-color: ${props => props.backgroundColor || DEFAULT_STYLES.backgroundColor};
  color: ${props => props.textColor || DEFAULT_STYLES.color};
  font-size: ${DEFAULT_STYLES.fontSize};
  border-radius: ${DEFAULT_STYLES.borderRadius};
  font-weight: ${DEFAULT_STYLES.fontWeight};
  font-family: ${DEFAULT_STYLES.fontFamily};

  border: 0;
  
  &:disabled {
    background-color: #F3F6F9;
    color: #B4B4B4;
  }
`;