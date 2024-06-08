import styled from 'styled-components';
import {ButtonSecondaryStyles} from './props.ts';
import {DEFAULT_STYLES} from './config.ts';

export const ButtonContainer = styled.button<ButtonSecondaryStyles>`
  background-color: ${props => props.backgroundColor || DEFAULT_STYLES.backgroundColor};
  color: ${props => props.textColor || DEFAULT_STYLES.color};
  font-size: ${DEFAULT_STYLES.fontSize};
  border-radius: ${props => props.borderRadius || DEFAULT_STYLES.borderRadius};
  font-weight: ${DEFAULT_STYLES.fontWeight};
  font-family: ${DEFAULT_STYLES.fontFamily};
  
  border-width: 1px;
  border-style: solid;
  border-color: ${props => props.borderColor || props.textColor || DEFAULT_STYLES.borderColor};
  
  box-sizing: border-box;
  width: ${props => props.width};
  height: ${props => props.height};
  
  flex: ${props => props.flex};
  
  cursor: pointer;
  
  &:disabled {
    background-color: #F3F6F9;
    color: #B4B4B4;
  }
`;