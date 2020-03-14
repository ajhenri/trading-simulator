import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';

import Navigation from './Navigation';
import Activity  from './Activity';
import Account from './Account';
import Trade from './Trade';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

const mapStateToProps = (state) => {
    return {};
};

class Main extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidMount(){}

    render() {
        return (
            <Router>
                <div className="row">
                    <Navigation />
                    <div className="col-sm">
                        <Route exact path="/">
                            <Redirect to="/account"/>
                        </Route>
                        <Route path="/account" component={Account}/>
                        <Route path="/trade" component={Trade}/>
                        <Route path="/activity" component={Activity}/>
                    </div>
                </div>
            </Router>
        );
    }
}

const mapDispatchToProps = (dispatch) => {
    return bindActionCreators(
        {},
        dispatch
    );
};

export default connect(mapStateToProps, mapDispatchToProps)(Main);