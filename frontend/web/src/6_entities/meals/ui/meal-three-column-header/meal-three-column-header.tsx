import {MealThreeColumnHeaderProps} from './props';
import {SubTitles, Title} from './styles';

export function MealThreeColumnHeader(props: MealThreeColumnHeaderProps){
  return (
    <>
      <Title aria-colspan={3}>
        <td>
          {props.mealName}
        </td>
      </Title>
      <SubTitles>
        <td>{'Платно'}</td>
        <td>{'Льготно'}</td>
        <td>{'Общее'}</td>
      </SubTitles>
    </>
  );
}
