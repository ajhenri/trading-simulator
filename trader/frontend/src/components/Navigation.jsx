import React from 'react';
import { withRouter } from 'react-router';

import StockSearch from './StockSearch';

import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Form from 'react-bootstrap/Form';
import NavDropdown from 'react-bootstrap/NavDropdown';

class Navigation extends React.Component {
    constructor(props) {
        super(props);
        this.selectStock = this.selectStock.bind(this);
    }

    selectStock(stock){
        if(stock){
            this.props.setStockSymbol(stock.symbol);
            this.props.history.push('/trade?quote=' + stock.symbol);
        }
    }

    render() {
        const user = document.getElementsByName('logged_in_user')[0];

        return (
            <Navbar collapseOnSelect bg="light" expand="lg" fixed="top" className="navbar-custom">
                <Navbar.Brand href="/account">Trader</Navbar.Brand>
                <Navbar.Toggle aria-controls="trader-navbar" />
                <Navbar.Collapse id="trader-navbar" className="justify-content-end">
                    <Nav className="mr-auto">
                        <Form inline>
                            <StockSearch selectStock={this.selectStock} />
                        </Form>
                    </Nav>
                    <Nav>
                        <NavDropdown title={user.value} id="nav-dropdown">
                            <NavDropdown.Item href="/account">
                                My Account
                            </NavDropdown.Item>
                            <NavDropdown.Item href="/activity">
                                My Activity
                            </NavDropdown.Item>
                            <NavDropdown.Divider />
                            <NavDropdown.Item href="/logout">
                                Logout
                            </NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        );
    }
}

export default withRouter(Navigation);