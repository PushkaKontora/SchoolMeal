import {SchoolClass} from '../../school-class/model/school-class';
import {MealPlan} from './meal-plan';

export type Child = {
    id: string,
    lastName: string,
    firstName: string,
    schoolClass: SchoolClass,
    mealPlan: MealPlan
}
