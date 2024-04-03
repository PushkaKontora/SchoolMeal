import {SwitchCellProps} from './props.ts';
import {AbstractCell, ContentContainer} from '../../abstract-cell';
import {Switch, SwitchProps} from '../../../interactive/switch';

export function SwitchCell(props: SwitchCellProps) {
  const switchProps = props as SwitchProps;
  return (
    <AbstractCell
      {...props.cellProps}>
      <ContentContainer
        $justifyContent={'center'}>
        <Switch
          toggled={switchProps.toggled}
          onToggle={switchProps.onToggle}
          disabled={switchProps.disabled}/>
      </ContentContainer>
    </AbstractCell>
  );
}
