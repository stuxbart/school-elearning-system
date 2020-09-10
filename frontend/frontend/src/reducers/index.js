import { combineReducers } from 'redux';

import styleReducer from './styleReducer';
import authReducer from './authReducer';
import messageReducer from './messageReducer';

export default combineReducers({
    style: styleReducer,
    auth: authReducer,
    messages: messageReducer,
})