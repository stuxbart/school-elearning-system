import React from 'react';
import { Message } from 'semantic-ui-react';

const colors = {
    'error': 'red',
    'info': 'blue',
    'success':'green',
}

const MessageBar = ({ header, list, body, type, onDismiss }) => {
    return <Message
    floating
    style={{marginTop: '70px', position: 'absolute', width: '100%'}}
    color={colors[type]}
    header={header} 
    list={list}
    content={body}
    onDismiss={() => onDismiss(type)}
    />
}

export default MessageBar;