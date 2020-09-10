import {
    SHOW_MESSAGE,
    HIDE_MESSAGE
} from './types';

export const showMessage = (message, type='INFO') => {
    return {
        type: SHOW_MESSAGE,
        payload: {
            type: type,
            body: message
        }
    }
}

export const showErrorMessage = (message) => {
    return showMessage(message, 'ERROR')
}

export const showSuccessMessage = (message) => {
    return showMessage(message, 'SUCCESS')
}

export const showInfoMessage = (message) => {
    return showMessage(message, 'INFO')
}

export const hideMessage = (type) => {
    return {
        type: HIDE_MESSAGE,
        payload: {
            type: type
        }
    }
}