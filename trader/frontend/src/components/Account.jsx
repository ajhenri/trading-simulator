import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { formatCurrency } from 'utils';
import { getAccountInfo } from 'actions';
import { ArrowUp } from 'react-bootstrap-icons';

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
        console.log(accountInfo);

        //{formatCurrency(accountInfo.equity_amount)}

        return (
            <div className="full-width">
                {accountInfoError && accountInfoError.status == 404 &&
                    <AccountCreationForm getAccountInfo={this.props.getAccountInfo}/>
                }
                {accountInfo &&
                    <div className="account-info">
                        <div className="account-total">
                            <h3>
                                {formatCurrency(accountInfo.cash_amount)}
                            </h3>
                            <small className="account-pct-change">
                                <ArrowUp color="royalblue" size={24}/>43.9%
                            </small>
                        </div>
                        
                        <h5>Positions</h5>
                        <p className="text-muted">No positions currently held.</p>
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