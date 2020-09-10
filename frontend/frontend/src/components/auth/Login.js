import React from 'react';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import { Button, Form, Grid, Header, Message, Segment, Checkbox } from 'semantic-ui-react';

import { setFixedNavbar, login } from '../../actions';

class Login extends React.Component {
  state = { 
    username: '', 
    password: '',
    rememberMe: false
  }
  componentDidMount() {
    this.props.setFixedNavbar()
  }
  onFormSubmit(event) {
    event.preventDefault();
    this.props.login(this.state.username, this.state.password, this.state.rememberMe);
  }
  render() {
    if (this.props.auth.isAuthenticated) {
      return <Redirect to='/' />
    }
    return (
      <Grid textAlign='center' style={{ height: '100vh' }} verticalAlign='middle'>
      <Grid.Column style={{ maxWidth: 450 }}>
        <Header as='h2' color='teal' textAlign='center'>
          Log-in to your account
        </Header>
        <Form size='large' onSubmit={(e) => this.onFormSubmit(e)}>
          <Segment stacked>
            <Form.Input 
              fluid 
              icon='user' 
              iconPosition='left' 
              placeholder='E-mail address' 
              onChange={e => this.setState({ username: e.target.value })}
              value={this.state.username}
            />
            <Form.Input
              fluid
              icon='lock'
              iconPosition='left'
              placeholder='Password'
              type='password'
              onChange={e => this.setState({ password: e.target.value })}
              value={this.state.password}
            />
            <Form.Field
            control={Checkbox}
            label="Remember me"
            onChange={(e, data) => this.setState({ rememberMe: data.checked })}
            checked={this.props.rememberMe}
            />
            <Button color='teal' fluid size='large'>
              Login
            </Button>
          </Segment>
        </Form>
        <Message>
          New to us? <a href='#'>Sign Up</a>
        </Message>
      </Grid.Column>
    </Grid>
    )
  }
};

const mapStateToProps = (state) => {
    return {
        auth: state.auth
    }
};


export default connect(mapStateToProps, {setFixedNavbar, login})(Login);