import styled from 'styled-components';

export const TableContainer = styled.table<{
  $width?: string
}>`
  width: ${props => props.$width || '100%'};
  overflow-x: auto;
  overflow-y: scroll;
  
  border-collapse: collapse;
`;
