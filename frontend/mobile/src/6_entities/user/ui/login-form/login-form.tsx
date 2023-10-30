import {useForm, Controller} from 'react-hook-form';
import {View} from 'react-native';
import {LoginFormProps} from './props';
import {createStyle} from './style';
import {ButtonPrimary} from '../../../../7_shared/ui/buttons/button-primary';
import {InputField} from '../../../../7_shared/ui/fields/input-field';
import {INPUT_DATA} from './input-data';
import {LoginFormData} from './types';
import {useState} from 'react';

export function LoginForm(props: LoginFormProps) {
  const {
    handleSubmit,
    control,
    formState: {errors}
  } = useForm<LoginFormData>({
    mode: 'onChange'
  });

  const [disabled, setDisabled] = useState(false);

  const styles = createStyle();

  const onSubmit = (currentData: LoginFormData) => {
    setDisabled(true);
    props.onSubmit(currentData);
  };

  return (
    <View style={styles.container}>

      <View style={styles.form}>

        <Controller
          control={control}
          name={INPUT_DATA[0].name}
          rules={INPUT_DATA[0].options}
          render={({field: {onChange, value}}) => (
            <InputField
              data={INPUT_DATA[0]}
              onChangeText={onChange}
              value={value}
              errors={errors}/>
          )} />

        <Controller
          control={control}
          name={INPUT_DATA[1].name}
          rules={INPUT_DATA[1].options}
          render={({field: {onChange, value}}) => (
            <InputField
              data={INPUT_DATA[1]}
              onChangeText={onChange}
              value={value}
              errors={errors}/>
          )} />

      </View>

      <ButtonPrimary
        disabled={disabled}
        title={'Войти'}
        onPress={handleSubmit(onSubmit)}/>

    </View>
  );
}
