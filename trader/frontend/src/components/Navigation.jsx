import React from 'react';
import { withRouter } from 'react-router';

import StockSearch from './StockSearch';

import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Form from 'react-bootstrap/Form';
import Dropdown from 'react-bootstrap/Dropdown';

class Navigation extends React.Component {
    constructor(props) {
        super(props);
        this.selectStock = this.selectStock.bind(this);
    }

    selectStock(stock){
        if(stock){
            this.props.setStockSymbol(stock.symbol);
            this.props.getStockInfo(stock.symbol);
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
                    <Nav>
                        <Form inline>
                            <StockSearch selectStock={this.selectStock} />
                        </Form>
                        <Dropdown id="nav-dropdown" alignRight>
                            <Dropdown.Toggle id="user-dropdown" as={Nav.Link}>
                                {user.value}
                            </Dropdown.Toggle>
                            <Dropdown.Menu>
                                <Dropdown.Item href="/account">
                                    My Account
                                </Dropdown.Item>
                                <Dropdown.Item href="/activity">
                                    My Activity
                                </Dropdown.Item>
                                <Dropdown.Divider />
                                <Dropdown.Item href="/logout">
                                    Logout
                                </Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        );
    }
}

export default withRouter(Navigation);