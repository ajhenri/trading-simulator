import React from 'react';
import PropTypes from 'prop-types';

import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { setStockSymbol } from 'actions';
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';

import Navigation from './Navigation';
import Activity  from './Activity';
import Account from './Account';
import Trade from './Trade';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

class Main extends React.Component {
    constructor(props, context) {
        super(props, context);
    }
    
    render() {
        return (
            <Router>
                <Navigation setStockSymbol={this.props.setStockSymbol}/>
                <Container className="container-main">
                    <Row>
                        <Route exact path="/">
                            <Redirect to="/account"/>
                        </Route>
                        <Route path="/account" render={(props) => <Account {...props} />} />
                        <Route path="/trade" render={(props) => <Trade {...props} setStockSymbol={this.props.setStockSymbol} />} />
                        <Route path="/activity" render={(props) => <Activity {...props} />} />
                    </Row>
                </Container>
            </Router>
        );
    }
}

Main.propTypes = {
    selectedStockSymbol: PropTypes.string
};

const mapStateToProps = (state) => {
    return {
        selectedStockSymbol: state.selectedStockSymbol
    };
};

const mapDispatchToProps = (dispatch) => {
    return bindActionCreators(
        { setStockSymbol },
        dispatch
    );
};

export default connect(mapStateToProps, mapDispatchToProps)(Main);