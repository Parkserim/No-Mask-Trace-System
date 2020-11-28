import React, { Component } from 'react';
import { Link, } from "react-router-dom";
import { logout } from '../actions/auth';
import { connect } from 'react-redux'; // added
import { Menu, Grid } from 'semantic-ui-react'

class Side extends Component {
  state = { activeItem: 'login' }


  handleItemClick = (e, { name }) => {
    this.setState({ activeItem: name })
  }

  render() {
    const { activeItem } = this.state
    const { isAuthenticated } = this.props.auth; // added 

    // added
    const userLinks = (
      <div>
        <Link onClick={this.props.logout} color='blue' >
          Logout
        </Link>
      </div>
    );

    const guestLinks = (
      <div >
        <Link to='/login'>
          Login
        </Link>
      </div>
    );

    return (
      <div style={{ paddingTop: "4rem", marginLeft: "2rem" }}>
        <h1 style={{ marginLeft: "1rem" }}>Mask Police</h1>
        <br></br>
        <Grid>
          <Grid.Column width={11}>
            <Menu fluid vertical tabular style={{ fontSize: "18px" }}>
              <Menu.Item
                name='login'
                active={activeItem === 'login'}
                onClick={this.handleItemClick}>
                {isAuthenticated ? userLinks : guestLinks}
              </Menu.Item>
              <Menu.Item
                name='File List'
                active={activeItem === 'File List'}
                onClick={this.handleItemClick}
              >
                <Link to="/files">File List</Link>
              </Menu.Item>

              <Menu.Item
                name='Device List'
                active={activeItem === 'Device List'}
                onClick={this.handleItemClick}
              >
                <Link to="/devices">Device List</Link>
              </Menu.Item>

              <Menu.Item
                name='Face List'
                active={activeItem === 'Face List'}
                onClick={this.handleItemClick}
              >
                <Link to="/faces">Face List</Link>
              </Menu.Item>
            </Menu>
          </Grid.Column>
        </Grid>
      </div>
    );
  }
}

// added
const mapStateToProps = state => ({
  auth: state.auth
});

// updated
export default connect(
  mapStateToProps,
  { logout }
)(Side);
