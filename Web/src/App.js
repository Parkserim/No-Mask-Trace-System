import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Files from './components/Files.js';
import Devices from './components/Devices.js';
import Side from './components/Side.js';
import Detail from './components/Detail.js';
import Faces from './components/Faces.js';
import Face from './components/Face.js';


import 'semantic-ui-css/semantic.min.css';
import LoginForm from './components/auth/LoginForm';
import PrivateRoute from './components/common/PrivateRoute';
import { Provider } from 'react-redux';
// import { loadUser } from './actions/auth'; // added
import store from './store';
import axios from "axios";
import { Grid } from 'semantic-ui-react'
import DeviceCreate from './components/DeviceCreate.js';

class App extends Component {
  // const host = "http://ec2-13-209-88-225.ap-northeast-2.compute.amazonaws.com"
  // componentDidMount() {
  //   store.dispatch(loadUser());
  // }

  render() {
    // axios.defaults.baseURL = 'http://192.168.1.8:8000/api';
    axios.defaults.baseURL = "http://ec2-13-209-88-225.ap-northeast-2.compute.amazonaws.com/api"
    return (
      <Grid>
        <Provider store={store}>
          <Router>
            <Grid.Column width={3}>
              <Side />
            </Grid.Column>
            <Grid.Column width={13} >
              <div style={{ marginTop: "9rem", paddingRight: "9rem" }}>
                <Route exact path='/login' component={LoginForm} />
                <PrivateRoute path="/files" component={Files} />
                <PrivateRoute path="/devices" component={Devices} />
                <PrivateRoute path="/detail/:pk" component={Detail} />
                <PrivateRoute path="/device_create" component={DeviceCreate} />
                <PrivateRoute path="/faces" component={Faces} />
                <PrivateRoute path="/face/:pk" component={Face} />
              </div>
            </Grid.Column>
          </Router>
        </Provider>
      </Grid >
    )
  }
}
export default App;
