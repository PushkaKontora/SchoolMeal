import styled from 'styled-components';
import {ValueBadgeStyles} from './props';
import {DEFAULT_BACKGROUND, DEFAULT_TEXT_COLOR, DEFAULT_WIDTH} from './config';

export const BadgeContainer = styled.div<ValueBadgeStyles>`
  background-color: ${props => props.backgroundColor || DEFAULT_BACKGROUND};
  color: ${props => props.textColor || DEFAULT_TEXT_COLOR};
  margin: ${props => props.margin || DEFAULT_TEXT_COLOR};
  
  font-family: 'Ubuntu';
  font-weight: 700;
  font-size: 14px;
  text-align: center;
  vertical-align: middle;
  padding: 4px 0;
  
  border-radius: 6px;
  width: ${props => props.width || DEFAULT_WIDTH};
`;
