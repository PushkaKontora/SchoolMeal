import {NutritionClassListProps} from './props.ts';
import {Container} from './styles.ts';
import {MealPlanPupilTable} from '../../../../6_entities/meal-plan';
import {TextCell} from '../../../../7_shared/ui/v2/table';
import {MealPlanStatusBadgeCell} from '../../../../6_entities/meal-plan';
import {SwitchCell} from '../../../../7_shared/ui/v2/table/cells/switch-cell';

export function NutritionClassList(props: NutritionClassListProps) {
  return (
    <Container>
      <MealPlanPupilTable
        data={props.data}
        tableData={props.tableData}
        updateData={props.updateData}
        cells={{
          HeaderTextCell: props => <TextCell
            text={props.title}
            cellProps={{
              key: props.key,
              header: true,
              cellStyles: {
                justifyContent: props.justifyContent,
                width: props.width,
                whiteSpace: props.whiteSpace
              }
            }}
            styles={{
              justifyContent: props.justifyContent
            }}
          />,
          ValueTextCell: props => <TextCell
            text={props.title}
            cellProps={{
              key: props.key,
              cellStyles: {
                whiteSpace: props.whiteSpace
              }
            }}
          />,
          StatusCell: props => <MealPlanStatusBadgeCell
            cellProps={{
              key: props.key,
              cellStyles: {
                width: props.width,
                whiteSpace: props.whiteSpace
              }
            }}
            status={props.status}
          />,
          SwitchCell: props => <SwitchCell
            cellProps={{
              key: props.key
            }}
            toggled={props.toggled}
            onToggle={props.onToggle}
            disabled={props.disabled}
          />
        }}/>
    </Container>
  );
}
