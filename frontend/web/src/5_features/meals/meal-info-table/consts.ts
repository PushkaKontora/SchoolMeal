import {Meal} from '../../../6_entities/meals/model/meal';

export const MEALS: Meal[] = [
  {
    id: 1,
    creatorId: 1,
    mealId: 1,
    createdAt: new Date(),
    date: '2023-06-13',
    schoolClass: {
      id: 1,
      number: 1,
      letter: 'А',
      hasBreakfast: true,
      hasLunch: true,
      hasDinner: true
    },
    pupils: [
      {
        id: '1',
        breakfast: true,
        lunch: true,
        dinner: true,
        preferential: false
      },
      {
        id: '1',
        breakfast: true,
        lunch: true,
        dinner: true,
        preferential: false
      }
    ]
  }
];
