import {
    LOGIN,
    LOGOUT,
    USER_LOADED
} from './types';

import { authApi } from './../apis';

import {
    showErrorMessage,
    showInfoMessage
} from './messageActions';


export const login = (username, password, remember=false) => async dispatch => {
    await authApi.post('login', { email:username, password:password })
    .then((response) => {
        dispatch({
            type: LOGIN,
            payload: {
                token: response.data.token,
                user: response.data.user
            }
        });
        if (remember) {
            localStorage.setItem('token', response.data.token);
        }
        
    })
    .catch((error) => {
        if (error.response) {
            console.log(error.response.data)
            dispatch(showErrorMessage("LOGIN ERROR"))
        }
        
    })
}

export const logout = () => async (dispatch, getState) => {
    const token = getState().auth.token
    const headers = {
        'Authorization': `Token ${token}`
    }

    await authApi.post('logout', {}, { headers:headers })
    .then((response) => {
        dispatch({
            type: LOGOUT
        })
        dispatch(showInfoMessage("LOGGED OUT"))
    })
    .catch((error) => {
        if (error.response) {
            console.log(error.response.data);
        }
    })
}

export const loadUser = () => async (dispatch, getState) => {
    const token = getState().auth.token
    const headers = {
        'Authorization': `Token ${token}`
    }
    await authApi.get('user', {headers:headers})
    .then(response => {
        dispatch({
            type: USER_LOADED,
            payload: response.data
        });
    })
    .catch(error => {
        if (token){
            dispatch(showErrorMessage("Auth error"));
        }
        
    });

}