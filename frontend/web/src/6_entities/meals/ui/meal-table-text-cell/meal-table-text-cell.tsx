import {MealTableTextCellProps} from './props';
import {TextContainer} from './styles';

export function MealTableTextCell(props: MealTableTextCellProps) {
  return (
    <TextContainer>
      <td>
        {props.text}
      </td>
    </TextContainer>
  );
}
