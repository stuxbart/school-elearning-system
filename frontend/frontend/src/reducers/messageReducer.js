import {
    SHOW_MESSAGE,
    HIDE_MESSAGE
} from './../actions/types';

import _ from 'lodash';

const initialState = {
    info: [],
    error: [],
    success: [],
    default: []
}

export default (state=initialState, action) => {
    switch (action.type) {
        case SHOW_MESSAGE: {
            const payload = action.payload
            switch (payload.type) {
                
                case 'ERROR': {
                    return {
                        ...state,
                        error: [payload.body]
                    }
                }

                case 'INFO': {
                    return {
                        ...state,
                        info: [payload.body]
                    }
                }

                case 'SUCCESS': {
                    return {
                        ...state,
                        success: [payload.body]
                    }
                }

                default: {
                    return {
                        ...state,
                        default: [payload.body]
                    }
                }

            }
        }

        case HIDE_MESSAGE: {
            return _.omit(state, action.payload.type)
        }
        
        default:
            return state;
    }
}