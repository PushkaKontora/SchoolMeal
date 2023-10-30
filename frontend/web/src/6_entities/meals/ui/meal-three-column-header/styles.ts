import styled from 'styled-components';

export const Title = styled.tr`
  width: 100%;
  height: 32px;
  
  background-color: #F3F6F9;

  letter-spacing: 0.03em;
  
  td {
    font-family: 'Ubuntu';
    font-size: 16px;
    font-weight: 800;

    color: #464E5F;
    
    text-align: center;
    vertical-align: top;
    
    padding-top: 10px;
  }
`;

export const SubTitles = styled.tr`
  width: 100%;
  height: 28px;

  background-color: #F3F6F9;
  
  display: flex;
  flex-direction: row;
  
  font-family: 'Ubuntu';
  font-size: 14px;
  font-weight: 800;

  color: rgba(70, 78, 95, 0.7);

  letter-spacing: 0.03em;
  
  td {
    flex: 1;
    
    text-align: center;
    vertical-align: bottom;
    
    padding-bottom: 10px;
  }
  
  td:last-child {
    color: #58BCBB;
  }
`;
