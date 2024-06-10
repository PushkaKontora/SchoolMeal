import styled from 'styled-components';
import {NotificationBadgeProps} from '../model/props.ts';

const Badge = styled.div<{
  count?: number
}>`
  background-color: #EC662A;
  border-radius: 4px;
  
  padding: 4px 8px;
  
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 12px;
  color: #FFFFFF;
  
  text-align: center;
  
  display: ${props => props.count ? 'block' : 'none'};
`;

export function NotificationBadge(props: NotificationBadgeProps) {
  return (
    <Badge
      count={props.value?.count}>
      {props.value?.count}
    </Badge>
  );
}
