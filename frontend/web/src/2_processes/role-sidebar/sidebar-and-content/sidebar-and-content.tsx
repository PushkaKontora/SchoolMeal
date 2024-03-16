import {Content, ParentContainer} from './styles.ts';
import {SidebarWithContentProps} from './props.ts';
import {PaddingArea} from '../../../7_shared/ui/v2/markup/padding-area';
import {SIDEBAR_WIDTH} from './config.ts';

export function SidebarAndContent(props: SidebarWithContentProps) {
  return (
    <ParentContainer
      $sidebarWidth={props.sidebarWidth || SIDEBAR_WIDTH}>
      {props.shouldShowSidebar && props.sidebar}
      <Content
        $sidebarWidth={props.sidebarWidth || SIDEBAR_WIDTH}>
        <PaddingArea
          padding={props.contentStyles?.padding}>
          {props.children}
        </PaddingArea>
      </Content>
    </ParentContainer>
  );
}
