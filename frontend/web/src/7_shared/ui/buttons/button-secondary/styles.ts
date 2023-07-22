import styled from 'styled-components';
import {ButtonSecondaryStyles} from './props';
import {DEFAULT_STYLES} from './config';

export const ButtonContainer = styled.button<ButtonSecondaryStyles>`
  padding: ${DEFAULT_STYLES.padding};
  background-color: ${DEFAULT_STYLES.backgroundColor};
  color: ${DEFAULT_STYLES.color};
  font-size: ${DEFAULT_STYLES.fontSize};
  border-radius: ${DEFAULT_STYLES.borderRadius};
  font-weight: ${DEFAULT_STYLES.fontWeight};
  font-family: ${DEFAULT_STYLES.fontFamily};
`;