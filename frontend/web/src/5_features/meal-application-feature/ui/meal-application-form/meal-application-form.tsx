import {Container, Header, StatusContainer, TableContainer} from './styles.ts';
import {MealRequestList, MealRequestStatusBadge} from '../../../../6_entities/meal-request';
import {MealApplicationFormProps} from './props.ts';
import {MealPlanHeaderCell} from '../../../../6_entities/meal-plan/ui/meal-plan-header-cell';
import {CancelledNutritionBadgeCell} from '../../../../6_entities/pupil';
import {ButtonPrimary} from '../../../../7_shared/ui/v2/interactive/buttons/button-primary';

export function MealApplicationForm(props: MealApplicationFormProps) {
  return (
    <Container>
      <Header>
        <StatusContainer>
          <MealRequestStatusBadge
            status={props.status}/>
        </StatusContainer>
        <ButtonPrimary
          borderRadius={'100px'}
          width={'270px'}
          height={'40px'}
          title={props.buttonTitles[props.status]}
          onPress={props.onSend}/>
      </Header>
      <TableContainer>
        <MealRequestList
          data={props.data}
          updateData={props.updateData}
          headerViewData={props.headerViewData}
          cells={{
            mealPlanHeader: props => (
              <MealPlanHeaderCell
                key={props.key}
                title={props.title}
                price={props.price.toString()}/>
            ),
            cancelledBadge: props => (
              <CancelledNutritionBadgeCell
                key={props.key}
                text={'снят родителем'}
                cancelled={props.cancelled}/>
            )
          }}/>
      </TableContainer>
    </Container>
  );
}
