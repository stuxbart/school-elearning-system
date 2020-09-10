import React from 'react';
import { connect } from 'react-redux';

import MessageBar from './MessageBar';
import { hideMessage } from '../../actions';



class Messages extends React.Component {
    onDismiss = (type) => {
        this.props.hideMessage(type)
    }
    render() {
        const messages = this.props.messages
        const renderedMessages = []
        for(var prop in messages) {
            const message = messages[prop]
            if (message.length > 0) {
                renderedMessages.push(
                <MessageBar
                key={prop}
                type={prop} 
                list={message} 
                onDismiss={this.onDismiss}
                />)
            }
        }
        return renderedMessages;
    }
}

const mapStateToProps = (state) => {
    return {
        messages: state.messages
    }
}
export default connect(mapStateToProps, {hideMessage})(Messages);