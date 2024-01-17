import {LoginFormData} from './types';
import {useForm} from 'react-hook-form';
import {FieldContainer, FormContainer, InputLabelStyled} from './styles';
import {INPUT_DATA} from './input-data';
import {ControlledInputField} from '../../../../7_shared/ui/fields/controlled-input-field/controlled-input-field';
import {ButtonPrimary} from '../../../../7_shared/ui/buttons/button-primary';
import {useState} from 'react';
import {LoginFormProps} from './props';

export function LoginForm(props: LoginFormProps) {
  const {
    handleSubmit,
    control,
    formState: {errors}
  } = useForm<LoginFormData>({
    mode: 'onChange'
  });

  const [disabled, setDisabled] = useState(false);

  const onSubmit = (data: LoginFormData) => {
    setDisabled(true);
    props.onSubmit(data);
  };

  return (
    <FormContainer>
      {
        INPUT_DATA.map((item) => (
          <FieldContainer
            key={item.name}>
            <InputLabelStyled>
              {item.label}
            </InputLabelStyled>

            <ControlledInputField
              key={item.name}
              control={control}
              errors={errors}
              data={item}/>
          </FieldContainer>
        ))
      }

      <ButtonPrimary
        title={'Далее'}
        fontSize={'24px'}
        onPress={handleSubmit(onSubmit)}
        disabled={disabled}/>

    </FormContainer>
  );
}