import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { formatCurrency } from 'utils';
import { getAccountInfo } from 'actions';

import 'css/account.css';
import AccountCreationForm from './AccountCreationForm';

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

        return (
            <div className="row section-body">
                <div className="col-sm">
                    {accountInfoError && accountInfoError.status == 404 &&
                        <AccountCreationForm getAccountInfo={this.props.getAccountInfo}/>
                    }
                    {accountInfo &&
                        <div className="account-info">
                            <h5>Account</h5>
                            <label>Cash: {formatCurrency(accountInfo.cash_amount)}</label>
                            <br/>
                            <label>Equity: {formatCurrency(accountInfo.equity_amount)}</label>
                            <hr></hr>
                            <h5>Stock Portfolio</h5>
                            <p className="text-muted">No positions currently held.</p>
                        </div>
                    }
                </div>
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