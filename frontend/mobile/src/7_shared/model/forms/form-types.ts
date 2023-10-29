import {Control, FieldErrors} from 'react-hook-form';
import {LegacyRef} from 'react';
import {TextInput} from 'react-native';

export type FormDataOptions = any;

export type FormControl = Control<any, any>;
export type FormErrors = FieldErrors;
export type FormRegister = any;
export type FormOnChangeText = any;
export type FormInputRef = LegacyRef<TextInput>
