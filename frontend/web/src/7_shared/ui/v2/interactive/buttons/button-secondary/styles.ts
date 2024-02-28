import styled from 'styled-components';
import {ButtonSecondaryStyles} from './props.ts';
import {DEFAULT_STYLES} from './config.ts';

export const ButtonContainer = styled.button<ButtonSecondaryStyles>`
  padding: ${DEFAULT_STYLES.padding};
  background-color: ${props => props.backgroundColor || DEFAULT_STYLES.backgroundColor};
  color: ${props => props.textColor || DEFAULT_STYLES.color};
  font-size: ${DEFAULT_STYLES.fontSize};
  border-radius: ${DEFAULT_STYLES.borderRadius};
  font-weight: ${DEFAULT_STYLES.fontWeight};
  font-family: ${DEFAULT_STYLES.fontFamily};
  border: 1px solid ${props => props.textColor || DEFAULT_STYLES.borderColor};
  
  box-sizing: border-box;
  width: ${props => props.width};
  height: ${props => props.height};
  
  &:disabled {
    background-color: #F3F6F9;
    color: #B4B4B4;
  }
`;