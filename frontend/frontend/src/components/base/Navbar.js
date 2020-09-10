import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { Menu, Button, Container } from 'semantic-ui-react'

import SearchBar from '../common/SearchBar';


class Navbar extends React.Component {
    renderRightPanel() {
        const fixed = this.props.style.navbar.fixed
        const auth = this.props.auth
        if (auth.isAuthenticated) {
            const visibleName = auth.user.full_name ? auth.user.full_name : auth.user.user_index
            return (
                <>
                <Menu.Item position='right' as='a'>
                    {visibleName}
                </Menu.Item>
                <Menu.Item position='right'>
                    <Button to="/logout" as={Link} inverted={!fixed}>Logout</Button>
                </Menu.Item>
                </>
            );
        }
        return (
            <Menu.Item position='right'>
                <Button to="/login" as={Link} inverted={!fixed}>Log in</Button>
                <Button color='teal' style={{ marginLeft: '0.5em' }} inverted={!fixed}>Sign Up</Button>
            </Menu.Item>
        );
    }
    render() {
        const style = {height: '45px'}
        const fixed = this.props.style.navbar.fixed
        return (
            <Menu
                fixed='top'
                color={fixed ?'teal':'black'}
                secondary
                pointing={true}
                style={fixed?{backgroundColor: 'white'}:{}}
                inverted={!fixed}
                >
                <Container>
                    <Menu.Item as={Link} to='/' active style={style}>Home</Menu.Item>
                    <Menu.Item as='a' style={style}>Work</Menu.Item>
                    <Menu.Item as='a' style={style}>Company</Menu.Item>
                    <Menu.Item as='a' style={style}>Careers</Menu.Item>
                    <Menu.Item position='right'><SearchBar transparent={!fixed} /></Menu.Item>
                    {this.renderRightPanel()}
                </Container>
            </Menu>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        style: state.style,
        auth: state.auth
    }
}

export default connect(mapStateToProps)(Navbar);
