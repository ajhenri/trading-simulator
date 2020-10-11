import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { formatCurrency } from 'utils';
import { getAccountInfo } from 'actions';
import Table from 'react-bootstrap/Table';
import { ArrowUp } from 'react-bootstrap-icons';
import { Link } from 'react-router-dom';

import 'css/account.css';
import AccountCreationForm from './AccountCreationForm';
import Yahoo from '../images/yahoo.png';
import MW from '../images/marketwatch.png';

const mapStateToProps = (state) => {
    return {
        isRequestingAccountInfo: state.isRequestingAccountInfo,
        accountInfoError: state.accountInfoError,
        accountInfo: state.accountInfo
    };
};

class Account extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidMount(){
        this.props.getAccountInfo();
    }

    render() {
        const { accountInfo, accountInfoError } = this.props;
        console.log(accountInfo);

        const stocks = accountInfo != null ? accountInfo.stocks : {};
        const stocksKeys = Object.keys(stocks);
        const actChangeClass = accountInfo != null && parseFloat(accountInfo.pct_change) < 0 ? 'loss': 'gain';

        return (
            <div className="full-width">
                {accountInfoError && accountInfoError.status == 404 &&
                    <AccountCreationForm getAccountInfo={this.props.getAccountInfo}/>
                }
                {accountInfo &&
                    <div className="account-summary">
                        <div className="account-totals">
                            <div className="account-tile">
                                <label>Value:</label>
                                <p>{formatCurrency(accountInfo.total_amount)}</p>
                            </div>
                            <div className="account-tile">
                                <label>Gain/Loss:</label>
                                <p className={actChangeClass}>
                                    <ArrowUp color="royalblue" size={24}/>{accountInfo.pct_change}%
                                </p>
                            </div>
                            <div className="account-tile">
                                <label>Cash</label>
                                <p>{formatCurrency(accountInfo.cash_amount)}</p>
                            </div>
                        </div>

                        <div className="clearfix"/>
                        <h5>Positions</h5>
                        {stocksKeys.length > 0 
                            ?
                            <Table hover>
                                <thead>
                                    <tr>
                                        <th>Security</th>
                                        <th>Price</th>
                                        <th>Shares</th>
                                        <th>Cost</th>
                                        <th>Value</th>
                                        <th className="resource-col"></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {stocksKeys.map((symbol) => (
                                        <tr key={symbol}>
                                            <td>
                                                <Link to={'/trade?quote='+symbol}>{symbol}</Link>
                                            </td>
                                            <td>{stocks[symbol].price}</td>
                                            <td>{stocks[symbol].shares}</td>
                                            <td>{stocks[symbol].cost}</td>
                                            <td>{stocks[symbol].value}</td>
                                            <td className="resource-col">
                                                <a className="resource-link" target="_blank"
                                                    href={'https://finance.yahoo.com/quote/' + symbol}>
                                                    <img src={Yahoo}/>
                                                </a>
                                                <a className="resource-link" target="_blank"
                                                    href={'https://www.marketwatch.com/investing/stock/' + symbol}>
                                                    <img src={MW}/>
                                                </a>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </Table>
                            :
                            <p className="text-muted">No positions currently held.</p>
                        }
                    </div>
                }
            </div>
        );
    }
}

const mapDispatchToProps = (dispatch) => {
    return bindActionCreators(
        { getAccountInfo },
        dispatch
    );
}

export default connect(mapStateToProps, mapDispatchToProps)(Account);