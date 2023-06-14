import styled from 'styled-components';
import {ButtonPrimaryStyles} from './props';
import {DEFAULT_STYLES} from './config';

export const ButtonContainer = styled.button<ButtonPrimaryStyles>`
  padding: ${DEFAULT_STYLES.padding};
  background-color: ${DEFAULT_STYLES.backgroundColor};
  color: ${DEFAULT_STYLES.color};
  font-size: ${DEFAULT_STYLES.fontSize};
  border-radius: ${DEFAULT_STYLES.borderRadius};
  font-weight: ${DEFAULT_STYLES.fontWeight};
  font-family: ${DEFAULT_STYLES.fontFamily};

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
