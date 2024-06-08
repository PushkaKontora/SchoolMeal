import {SidebarBottomActions, SidebarContainer, SidebarItemList} from './styles.ts';
import {Logo} from '../logo/logo.tsx';
import {SidebarProps} from './props.ts';
import {SidebarIconedButton} from '../iconed-button';
import {LogoutButton} from '../logout-button';

export function Sidebar(props: SidebarProps) {
  return (
    <SidebarContainer>
      <Logo/>
      <SidebarItemList>
        {props.items.map((item, index) =>
          <SidebarIconedButton
            {...item}
            active={item.active || props.selectedItemIndex == index}
          />)}
      </SidebarItemList>
      <SidebarBottomActions>
        {props?.actionItems?.map(item =>
          <SidebarIconedButton {...item}/>)}
      </SidebarBottomActions>
      <LogoutButton
        {...props.logoutButtonProps}/>
    </SidebarContainer>
  );
}
