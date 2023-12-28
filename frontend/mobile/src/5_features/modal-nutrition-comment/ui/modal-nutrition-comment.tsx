import {Text, View} from 'react-native';
import {createStyles} from '../consts/styles';
import {InputFieldLimited} from '../../../7_shared/ui/controlled/input-field-limited';
import {MarginArea} from '../../../7_shared/ui/styling/margin-area';
import {ButtonPrimary} from '../../../7_shared/ui/buttons/button-primary';
import {ModalWindow} from '../../../7_shared/ui/modal/modal-window/ui/modal-window';
import {DESCRIPTION, TITLE} from '../../modal-meal-period/consts/text';
import {useForm} from 'react-hook-form';
import {INPUT_DATA} from '../consts/input-data';
import {DEFAULT_NUMBER_OF_LINES, DEFAULT_SYMBOL_LIMIT} from '../config/config';
import {useEffect} from 'react';
import {CommentFormData} from '../model/comment-form-data';
import {ModalNutritionCommentProps} from '../model/props';

export function ModalNutritionComment(props: ModalNutritionCommentProps) {
  const {
    handleSubmit,
    trigger,
    control,
    formState: {errors}
  } = useForm<CommentFormData>({
    mode: 'onChange'
  });

  const styles = createStyles();

  useEffect(() => {
    trigger();
  }, []);

  const onSubmit = (currentData: CommentFormData) => {
    if (props.onSendClick) {
      props.onSendClick(currentData);
    }
  };

  const submitWithoutComment = () => {
    if (props.onSendClick) {
      props.onSendClick({
        reason: undefined
      });
    }
  };

  return (
    <ModalWindow
      headerModalTitle={TITLE}
      showCloseButton={false}>
      <Text
        style={styles.text}>
        {DESCRIPTION}
      </Text>
      <MarginArea
        marginBottom={24}>
        <InputFieldLimited
          maxLength={DEFAULT_SYMBOL_LIMIT}
          numberOfLines={DEFAULT_NUMBER_OF_LINES}
          control={control}
          data={INPUT_DATA[0]}
          errors={errors}/>
      </MarginArea>
      <View
        style={styles.buttons}>
        <ButtonPrimary
          flex={1}
          fontSize={12}
          onPress={handleSubmit(onSubmit)}
          disabled={errors['reason'] !== undefined}
          title={'Отправить'}/>
        <ButtonPrimary
          flex={1}
          backgroundColor={'#F7F7F7'}
          textColor={'#2C2C2C'}
          fontSize={12}
          onPress={submitWithoutComment}
          title={'Без комментария'}/>
      </View>
    </ModalWindow>
  );
}
