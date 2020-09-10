import {
    LOGIN,
    LOGOUT,
    USER_LOADED
} from '../actions/types'

const initialState = {
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false,
}
export default (state=initialState, action) => {
    switch (action.type) {
        case LOGIN: {
            return {
                user: action.payload.user,
                token: action.payload.token,
                isAuthenticated: true,
            }
        }

        case LOGOUT: {
            localStorage.removeItem('token');
            return {
                isAuthenticated:false,
                user: null,
                token: null
            };
        }

        case USER_LOADED: {
            return {
                ...state,
                isAuthenticated: true,
                user: action.payload
            }
        }

        default: {
            return state
        }
    }
}