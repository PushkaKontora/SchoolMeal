import {RoleSidebarProps} from '../model/props.ts';
import {createItems} from '../lib/create-items.tsx';
import {useNavigate} from 'react-router-dom';
import {AppSidebar} from '../../../../4_widgets/app-sidebar';
import {useState} from 'react';

export function RoleSidebar(props: RoleSidebarProps) {
  const navigate = useNavigate();

  const [selectedItemIndex, setSelectedItemIndex] = useState(0);
  const items = createItems(setSelectedItemIndex, navigate, props.userRole);

  return (
    <AppSidebar
      selectedItemIndex={selectedItemIndex}
      userName={props.userName}
      items={items}
    />
  );
}
