import {CSSProperties} from 'react';
import styled from 'styled-components';

export const DEFAULT_STYLES: CSSProperties = {
  padding: '14px',
  fontWeight: '500',
  fontSize: '14px',
  color: '#FFFFFF',
  backgroundColor: '#EC662A',
  borderRadius: '10px',
  fontFamily: 'Roboto',
};

export const DefaultStyles = styled.button`
  padding: 14px;
  font-weight: 500;
  font-size: 14px;
  background-color: #EC662A;
  color: #FFFFFF;
  border-radius: 10px;
  font-family: 'Roboto', sans-serif;
`;
