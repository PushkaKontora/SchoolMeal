import styled from 'styled-components';
import {CSSProperties} from 'react';

export const TableContainer = styled.table<{
  $width?: CSSProperties['width']
}>`
  width: ${props => props.$width || '100%'};
  
  border-collapse: collapse;
  
  overflow-y: auto;
`;
