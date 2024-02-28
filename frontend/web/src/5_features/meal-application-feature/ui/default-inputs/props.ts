import {IMealApplicationFormInputs} from '../../model/meal-application-form-inputs.ts';

export type DefaultInputProps = {
  selectedClassIndex: number,
  classNames: string[]
} & IMealApplicationFormInputs;
