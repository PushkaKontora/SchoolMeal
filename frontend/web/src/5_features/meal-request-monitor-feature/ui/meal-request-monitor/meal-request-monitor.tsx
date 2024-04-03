import {MealRequestMonitorProps} from './props.ts';
import {Container} from './styles.ts';
import {MealRequestMonitorTable} from '../../../../6_entities/meal-request';
import {MealPlanValueBadgeCell} from '../../../../6_entities/meal-plan';

export function MealRequestMonitor(props: MealRequestMonitorProps) {
  return (
    <Container>
      <MealRequestMonitorTable
        data={props.data}
        cells={{
          CommonValueCell: props => (
            <MealPlanValueBadgeCell
              key={props.key}
              value={props.value}
              styles={{
                justifyContent: 'center'
              }}/>),
          TotalValueBadgeCell: props => (
            <MealPlanValueBadgeCell
              key={props.key}
              value={props.value}
              type={'total'}
              styles={{
                justifyContent: 'center'
              }}/>),
          FooterValueBadgeCell: props => (
            <MealPlanValueBadgeCell
              key={props.key}
              value={props.value}
              type={'totalInFooter'}
              styles={{
                justifyContent: 'center'
              }}/>)
        }}/>
    </Container>
  );
}
