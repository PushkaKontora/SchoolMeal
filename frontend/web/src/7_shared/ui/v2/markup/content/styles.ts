import styled from 'styled-components';
import {ContentStyles} from './props';
import {DEFAULT_WIDTH} from './config';

export const Container = styled.div<ContentStyles>`
  width: ${props => props.width || DEFAULT_WIDTH};
  height: 100%;
  
  min-width: 800px;
  
  margin: 0 auto;
`;
