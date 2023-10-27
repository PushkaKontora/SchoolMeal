import {MealTableHeaderProps} from './props';
import {Title} from './styles';

export function MealTableHeader(props: MealTableHeaderProps) {
  return (
    <Title
      height={props.height}
      fontSize={props.fontSize}>
      <td>
        {props.title}
      </td>
    </Title>
  );
}
