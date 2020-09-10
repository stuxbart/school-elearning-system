import {
    SET_FIXED_NAVBAR,
    UNSET_FIXED_NAVBAR
} from './types';


export const setFixedNavbar = () => {
    return {
        type: SET_FIXED_NAVBAR
    }
}

export const unsetFixedNavbar = () => {
    return {
        type: UNSET_FIXED_NAVBAR
    }
}