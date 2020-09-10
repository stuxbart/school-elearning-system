import React from 'react';
import Navbar from './Navbar';
import Messages from '../common/Messages';

class Base extends React.Component {
    handleItemClick = (e, { name }) => this.setState({ activeItem: name })
    state = {}

    render() {
        const { activeItem } = this.state

        return (
            <>
            <Navbar activeItem={activeItem} />
            <Messages />
            {this.props.children}
            </>
        );
    }
}

export default Base;