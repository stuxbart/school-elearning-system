import {
    SET_FIXED_NAVBAR,
    UNSET_FIXED_NAVBAR
} from '../actions/types';

const initialState = {
    navbar: {
        fixed: true
    }
}

export default (state=initialState, action) => {
    switch(action.type) {
        case SET_FIXED_NAVBAR: {
            return {
                ...state, 
                navbar: {
                    fixed: true
                }
            }
        }
        case UNSET_FIXED_NAVBAR: {
            return {
                ...state,
                navbar: {
                    fixed: false
                }
            }
        }
        default: {
            return state
        }
    }
}