import {useForm} from 'react-hook-form';
import {useState} from 'react';
import {SignUpFormData} from './types';
import {createStyle} from './style';
import {View} from 'react-native';
import {ButtonPrimary} from '../../../../7_shared/ui/buttons/button-primary';
import {ControlledInputField} from '../../../../7_shared/ui/controlled/controlled-input-field';
import {INPUT_DATA} from './input-data';
import {SignUpFormProps} from './props';

export function SignUpForm(props: SignUpFormProps) {
  const {
    handleSubmit,
    control,
    formState: {errors}
  } = useForm<SignUpFormData>({
    mode: 'onChange'
  });

  const [disabled, setDisabled] = useState(false);

  const styles = createStyle();

  const onSubmit = (data: SignUpFormData) => {
    setDisabled(true);
    props.onSubmit(data);
  };

  return (
    <View style={styles.container}>

      <View style={styles.form}>

        {
          INPUT_DATA.map((item) => (
            <ControlledInputField
              key={item.name}
              control={control}
              errors={errors}
              data={item}/>
          ))
        }

      </View>

      <ButtonPrimary
        disabled={disabled}
        title={'Зарегистрироваться'}
        onPress={handleSubmit(onSubmit)}/>

    </View>
  );
}
