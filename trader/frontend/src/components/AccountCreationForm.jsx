import React from 'react';
import ReactDOM from 'react-dom';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { createAccount } from 'actions';

import MaskedInput from 'react-text-mask';
import createNumberMask from 'text-mask-addons/dist/createNumberMask';

import { isEmpty } from 'utils';
import { validFld, invalidFld } from 'utils/forms';

const mapStateToProps = (state) => {
    return {
        isCreatingAccount: state.isCreatingAccount,
        createAccountError: state.createAccountError,
        account: state.account
    };
};

const numberMask = createNumberMask({
    prefix: '$',
    allowDecimal: true
});

class AccountCreationForm extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            initialAmount: '',
            fieldErrors: {}
        };

        this.handleFieldChange = this.handleFieldChange.bind(this);
        this.validateField = this.validateField.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount(){
        this.focusMaskedInput();
    }

    componentDidUpdate(prevProps){
        if(this.props.account && this.props.account.success){
            this.props.getAccountInfo();
        }
    }

    focusMaskedInput() {
        const {refs: {maskedInput}} = this
        ReactDOM.findDOMNode(maskedInput).focus()
    }

    validateField(field, name, value){
        let fieldErrors = this.state.fieldErrors;
        if(isEmpty(value)){
            fieldErrors[name] = `${field} is required`;
        } else {
            delete fieldErrors[name];
        }
        return this.setState({ fieldErrors });
    }

    handleFieldChange(event){
        const field = event.target.getAttribute('data-field');
        const name = event.target.name;
        const value = event.target.value;

        let state = this.state;
        state[name] = value;
        this.setState(state, () => {
            this.validateField(field, name, value);
        });
    }

    handleSubmit(event){
        event.preventDefault();

        if(Object.keys(this.state.fieldErrors).length > 0){
            return;
        }

        let initialAmount = this.state.initialAmount.match(/\d+/g).join([])
        if(isNaN(initialAmount)){
            const error = 'Starting Balance must be an amount.';
            return this.setState({ fieldErrors: { initialAmount: error } });
        } else if(initialAmount < 500){
            const error = 'Starting Balance must be at least $500.';
            return this.setState({ fieldErrors: { initialAmount: error } });
        }
        
        this.props.createAccount({
            initial_amount: initialAmount
        });
    }

    render() {
        const { fieldErrors } = this.state;
        
        let inputClass = 'form-control starting-balance-input';
        if(fieldErrors['initialAmount']){
            inputClass += ` ${invalidFld}`;
        }
        
        return (
            <div className="create-account form-small">
                <small>Enter an amount below and 
                    click "Create" to start a brokerage simulation account.</small>
                <form onSubmit={this.handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="initialAmount">
                            Starting Balance
                            <span className="text-danger">*</span>
                        </label>
                        <MaskedInput
                            data-field="Starting Balance"
                            className={inputClass}
                            name="initialAmount"
                            value={this.state.initialAmount}
                            ref="maskedInput"
                            mask={numberMask}
                            onChange={this.handleFieldChange}
                            required
                        />
                        <div>
                            <div className="text-danger error-message">{fieldErrors.initialAmount}</div>
                        </div>
                    </div>
                    <input type="submit" className="btn btn-primary" value="Create"/>
                </form>
            </div>
        );
    }
}

const mapDispatchToProps = (dispatch) => {
    return bindActionCreators(
        { createAccount },
        dispatch
    );
}

export default connect(mapStateToProps, mapDispatchToProps)(AccountCreationForm);