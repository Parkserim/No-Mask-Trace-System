import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import { Field, reduxForm } from 'redux-form';
import { login } from '../../actions/auth';
import { Button, Header, Grid, Segment, Form } from 'semantic-ui-react'

class LoginForm extends Component {
    usernameField = ({ input, label, type, meta: { touched, error } }) => {
        return (
            <div  >
                <Form.Input fluid {...input} icon='user' iconPosition='left' placeholder='User Name' />
            </div>
        );
    };

    passwordField = ({ input, label, type, meta: { touched, error } }) => {
        return (
            <div>
                <Form.Input
                    {...input}
                    fluid
                    icon='lock'
                    iconPosition='left'
                    placeholder='Password'
                    type='password'
                />
            </div>
        );
    };
    hiddenField = ({ type, meta: { error } }) => {
        return (
            <div >
                <br />
                <input type={type} />
                {error && <div  >{error}</div>}
                <br />
            </div>
        );
    };

    onSubmit = formValues => {
        this.props.login(formValues);
    };

    render() {
        if (this.props.isAuthenticated) {
            return <Redirect to='/' />;
        }
        return (
            <div style={{ marginTop: "13rem" }}>
                <Grid textAlign='center' verticalAlign='middle'>
                    <Grid.Column style={{ maxWidth: 450 }}>
                        <Header as='h2' color='blue' textAlign='center'>
                            관리자 로그인
                        </Header><br></br>
                        <Segment stacked>
                            <form
                                onSubmit={this.props.handleSubmit(this.onSubmit)}
                            >
                                <Field
                                    name='username'
                                    type='text'
                                    component={this.usernameField}
                                    label='Username'
                                />
                                <br />
                                <Field
                                    name='password'
                                    type='password'
                                    component={this.passwordField}
                                    label='Password'
                                />
                                <Field
                                    name='non_field_errors'
                                    type='hidden'
                                    component={this.hiddenField}
                                />
                                <Button color='blue' fluid size='large'>
                                    Login
                                </Button>
                            </form>
                        </Segment>
                    </Grid.Column>
                </Grid>
            </div>
        );
    }
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

LoginForm = connect(
    mapStateToProps,
    { login }
)(LoginForm);

export default reduxForm({
    form: 'loginForm'
})(LoginForm);