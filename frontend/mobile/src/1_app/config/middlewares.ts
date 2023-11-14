import middlewares from '../lib/middlewares/error-handler';
import {featuresMiddlewares} from '../../5_features/reducer';
import {entitiesMiddlewares} from '../../6_entities/reducer';

export const AppMiddlewares = [
  ...middlewares,
  ...featuresMiddlewares,
  ...entitiesMiddlewares
];
