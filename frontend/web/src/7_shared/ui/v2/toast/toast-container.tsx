import styled from 'styled-components';
import { ToastContainer } from 'react-toastify';
import {CloseButton} from './toast.tsx';

export const AppToastContainer = styled(ToastContainer).attrs({
  toastClassName: 'toast',
  bodyClassName: 'body',
  closeButton: buttonProps => <CloseButton onClick={buttonProps.closeToast}/>
})`
  .Toastify__toast-theme--colored.Toastify__toast--success {
    background-color: #F6FFF9;
    border: 1px solid #48C1B5;
  }

  .Toastify__toast-icon {
    width: 24px;
    height: 24px;
    
    margin-inline-end: 0;
  }
  
  .toast {
    font-family: 'Ubuntu', sans-serif;
    font-size: 14px;
    font-weight: 700;

    line-height: 19.6px;

    color: #27303A;
    
    padding: 20px;
    
    display: flex; !important;
    flex-direction: row; !important;
    align-items: center; !important;
    
    gap: 16px;
  }
  
  .body {
    padding: 0;
    
    display: flex;
    gap: 16px;
  }
`;
