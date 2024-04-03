import {Buttons, Container, Header, StatusContainer, TableContainer} from './styles.ts';
import {MealRequestApplicationList, MealRequestStatusBadge} from '../../../../6_entities/meal-request';
import {MealApplicationFormProps} from './props.ts';
import {MealPlanHeaderCell} from '../../../../6_entities/meal-plan';
import {CancelledNutritionBadgeCell} from '../../../../6_entities/pupil';
import {ButtonPrimary} from '../../../../7_shared/ui/v2/interactive/buttons/button-primary';
import {ButtonSecondary} from '../../../../7_shared/ui/v2/interactive/buttons/button-secondary';
import {MealApplicationFormStatus} from '../../../../6_entities/meal-request/model/meal-application-form-status.ts';

export function MealApplicationForm(props: MealApplicationFormProps) {
  return (
    <Container>
      <Header>
        <StatusContainer>
          <MealRequestStatusBadge
            status={props.status}/>
        </StatusContainer>
        <Buttons>
          {
            props.status === MealApplicationFormStatus.Edit && (
              <ButtonSecondary
                title={'Отмена'}
                width={'150px'}
                height={'40px'}
                onPress={props.onCancel}/>
            )
          }
          <ButtonPrimary
            borderRadius={'100px'}
            width={'270px'}
            height={'40px'}
            title={props.buttonTitles[props.status]}
            onPress={props.onSend}/>
        </Buttons>
      </Header>
      <TableContainer>
        <MealRequestApplicationList
          data={props.data}
          updateData={props.updateData}
          tableData={props.tableData}
          cells={{
            mealPlanHeader: props => (
              <MealPlanHeaderCell
                key={props.key}
                title={props.title}
                showContent={props.showContent}/>
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
