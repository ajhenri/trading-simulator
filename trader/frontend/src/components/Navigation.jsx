import React from 'react';
import { withRouter } from "react-router";
import { Link } from 'react-router-dom';

class Navigation extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const { location } = this.props;
        const section = location.state ? location.state.section : 'account';

        return (
            <nav className="col-md-2 d-none d-md-block bg-light sidebar">
                <div className="sidebar-sticky">
                    <ul className="nav nav-pills flex-column">
                        <li className="nav-item">
                            <Link className={section == "account" ? "nav-link active" : "nav-link"} to={{pathname: "/account", state: {section: 'account'}}}>
                                <svg className="bi bi-graph-up" width="32" height="32" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M2 2h1v16H2V2zm1 15h15v1H3v-1z"></path>
                                    <path fillRule="evenodd" d="M16.39 6.312l-4.349 5.437L9 8.707l-3.646 3.647-.708-.708L9 7.293l2.959 2.958 3.65-4.563.781.624z" clipRule="evenodd"></path>
                                    <path fillRule="evenodd" d="M12 5.5a.5.5 0 01.5-.5h4a.5.5 0 01.5.5v4a.5.5 0 01-1 0V6h-3.5a.5.5 0 01-.5-.5z" clipRule="evenodd"></path>
                                </svg>
                                Account
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link className={section == "trade" ? "nav-link active" : "nav-link"} to={{pathname: "/trade", state: {section: 'trade'}}}>
                                <svg className="bi bi-pie-chart-fill" width="32" height="32" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M17.985 10.5h-7.778l-5.5 5.5a8 8 0 0013.277-5.5zM4 15.292A8 8 0 019.5 2.015v7.778l-5.5 5.5zm6.5-13.277V9.5h7.485A8.001 8.001 0 0010.5 2.015z" clipRule="evenodd"/></svg>
                                Trade Stocks
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link className={section == "activity" ? "nav-link active" : "nav-link"} to={{pathname: "/activity", state: {section: 'activity'}}}>
                                <svg className="bi bi-table" width="32" height="32" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                    <path fillRule="evenodd" d="M16 3H4a1 1 0 00-1 1v12a1 1 0 001 1h12a1 1 0 001-1V4a1 1 0 00-1-1zM4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z" clipRule="evenodd"></path>
                                    <path fillRule="evenodd" d="M17 6H3V5h14v1z" clipRule="evenodd"></path>
                                    <path fillRule="evenodd" d="M7 17.5v-14h1v14H7zm5 0v-14h1v14h-1z" clipRule="evenodd"></path>
                                    <path fillRule="evenodd" d="M17 10H3V9h14v1zm0 4H3v-1h14v1z" clipRule="evenodd"></path>
                                    <path d="M2 4a2 2 0 012-2h12a2 2 0 012 2v2H2V4z"></path>
                                </svg>
                                Activity History
                            </Link>
                        </li>
                    </ul>
                </div>
            </nav>
        );
    }
}

export default withRouter(Navigation);