import React from 'react';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import { logout } from './../../actions';

const Logout = ({ isAuthenticated, logout }) => {
    if (isAuthenticated) {
        logout()
    }
    return <Redirect to='/' />;
};

const mapStateToProps = (state) => {
    return {
        isAuthenticated: state.auth.isAuthenticated
    }
}

export default connect(mapStateToProps, {logout})(Logout);