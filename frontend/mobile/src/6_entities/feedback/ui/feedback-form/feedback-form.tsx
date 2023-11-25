import {createStyle} from './limited-field-styles';
import {View} from 'react-native';
import {InputFieldLimited} from '../../../../7_shared/ui/controlled/input-field-limited';
import {ButtonPrimary} from '../../../../7_shared/ui/buttons/button-primary';
import {useForm} from 'react-hook-form';
import {INPUT_DATA} from './input-data';
import {FeedbackFormData} from './feedback-form-data';
import {DEFAULT_NUMBER_OF_LINES, DEFAULT_SYMBOL_LIMIT} from './config';
import {FeedbackFormProps} from './props';

export function FeedbackForm(props: FeedbackFormProps) {
  const {
    handleSubmit,
    control,
    formState: {errors}
  } = useForm<FeedbackFormData>({
    mode: 'onChange'
  });

  const styles = createStyle();

  const onSubmit = (currentData: FeedbackFormData) => {
    props.onSubmit(currentData);
  };

  return (
    <View
      style={styles.container}>
      <InputFieldLimited
        maxLength={props.symbolLimit || DEFAULT_SYMBOL_LIMIT}
        numberOfLines={DEFAULT_NUMBER_OF_LINES}
        control={control}
        data={INPUT_DATA[0]}
        errors={errors}
      />
      <ButtonPrimary
        title={props.buttonTitle}
        fontSize={12}
        fontWeight={'700'}
        paddingVertical={12}
        backgroundColor={'#EC662A'}
        onPress={handleSubmit(onSubmit)}/>
    </View>
  );
}
