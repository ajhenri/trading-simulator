import React from 'react';
import PropTypes from 'prop-types';

import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { searchStocks } from 'actions';

import { AsyncTypeahead } from 'react-bootstrap-typeahead';
import 'react-bootstrap-typeahead/css/Typeahead.css';

const mapStateToProps = (state) => {
    return {
        isRequestingStockSearch: state.isRequestingStockSearch ? state.isRequestingStockSearch : false,
        options: state.stockSearchResults ? state.stockSearchResults : []
    };
};

class StockSearch extends React.Component {

    constructor(props, context){
        super(props, context);

        this.state = {
            allowNew: false,
            multiple: false,
            value: ''
        };

        this.renderItem = this.renderItem.bind(this);
    }

    componentDidMount(){
        const symbol = this.props.selectedSymbol;
        if(symbol){
            this.props.searchStocks(symbol);
        }
    }

    renderItem(item, props){
        return (
            <div key={item.symbol}>
                {item.symbol + ' - ' + item.securityName}
            </div>
        );
    }

    render(){
        const { options, isRequestingStockSearch, selectStock } = this.props;
        const props = this.props;

        return (
            <div className="d-flex">
                <div className="d-inline-block">
                    <div className="search-container">
                        <svg className="bi bi-search search-icon" width="32" height="1em" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                            <path fillRule="evenodd" d="M12.442 12.442a1 1 0 011.415 0l3.85 3.85a1 1 0 01-1.414 1.415l-3.85-3.85a1 1 0 010-1.415z" clipRule="evenodd"></path>
                            <path fillRule="evenodd" d="M8.5 14a5.5 5.5 0 100-11 5.5 5.5 0 000 11zM15 8.5a6.5 6.5 0 11-13 0 6.5 6.5 0 0113 0z" clipRule="evenodd"></path>
                        </svg>
                        <AsyncTypeahead
                            {...this.state}
                            id="stock-search"
                            options={options}
                            labelKey="symbol"
                            className={"search-input"}
                            isLoading={isRequestingStockSearch}
                            minLength={1} 
                            onSearch={this.props.searchStocks}
                            onChange={(stockList) => {
                                const value = stockList[0];
                                this.setState({ value });
                                props.selectStock(value);
                            }}
                            placeholder="Enter a symbol..."
                            renderMenuItemChildren={this.renderItem}
                        />
                    </div>
                </div>
                <div className="d-inline-block">
                    <button className="ml-1 btn btn-light" type="button" onClick={props.selectStock}>Search</button>
                </div>
            </div>
        );
    }
}

StockSearch.propTypes = {
    selectStock: PropTypes.func
}

const mapDispatchToProps = (dispatch) => {
    return bindActionCreators(
        { searchStocks },
        dispatch
    );
}

export default connect(mapStateToProps, mapDispatchToProps)(StockSearch);