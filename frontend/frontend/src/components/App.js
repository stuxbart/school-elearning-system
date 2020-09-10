import React from 'react';
import { BrowserRouter, Route } from 'react-router-dom';
import { connect } from 'react-redux';

import Home from './home/Home';
import Login from './auth/Login';
import Logout from './auth/Logout';
import Base from './base/Base';

import { loadUser } from '../actions';

class App extends React.Component {
    componentDidMount() {
        this.props.loadUser();
    }
    render() {
        return (
            <BrowserRouter>
                <Base>
                    <Route path="/" exact component={Home} />
                    <Route path="/login" exact component={Login} />
                    <Route path="/logout" exact component={Logout} />
                </Base>
            </BrowserRouter>
        );
    }
}
export default connect(null, {loadUser})(App);