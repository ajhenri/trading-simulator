import React from 'react';
import PropTypes from 'prop-types';
import Autocomplete from 'react-autocomplete';

import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { searchStocks } from 'actions';

const mapStateToProps = (state) => {
    return {
        isRequestingStockSearch: state.isRequestingStockSearch,
        stockSearchResults: state.stockSearchResults ? state.stockSearchResults : []
    };
};

class StockSearch extends React.Component {

    constructor(props){
        super(props);

        this.state = {
            value: ''
        };

        this.autocomplete = React.createRef();
        this.renderItem = this.renderItem.bind(this);
        this.findSymbol = this.findSymbol.bind(this);
        this.getItemValue = this.getItemValue.bind(this);
        this.onChangeHandler = this.onChangeHandler.bind(this);
    }

    componentDidMount(){
        const symbol = this.props.selectedSymbol;
        if(symbol){
            this.props.searchStocks(symbol);
        }
    }

    findSymbol(symbol){
        const { stockSearchResults } = this.props;
        for(let i=0; i < stockSearchResults.length; i++){
            if(symbol == stockSearchResults[i].symbol){
                return stockSearchResults[i];
            }
        }
    }

    onChangeHandler(symbol){
        if(symbol != ''){
            this.props.searchStocks(symbol);
        }
    }

    renderItem(item, isHighlighted){
        let itemStyle = {
            padding: 5,
            cursor: 'pointer',
            background: 'white'
        };

        if(isHighlighted) itemStyle.background = 'lightgray';

        return (
            <div style={itemStyle} key={item.symbol}>
                {item.symbol + ' - ' + item.name}
            </div>
        );
    }

    getItemValue(item){
        return item.symbol + ' - ' + item.name;
    }

    render(){
        const { stockSearchResults } = this.props;

        const wrapperStyle = { 
            position: 'relative', 
            display: 'inline-block', 
            borderRadius: 5,
            zIndex: 100
        };

        const inputProps = { 
            id: 'symbol-search', 
            placeholder: 'Enter symbol',
            className: 'form-control'
        };

        return (
            <div className="form-group">
                <svg className="bi bi-search" width="32" height="1em" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path fillRule="evenodd" d="M12.442 12.442a1 1 0 011.415 0l3.85 3.85a1 1 0 01-1.414 1.415l-3.85-3.85a1 1 0 010-1.415z" clipRule="evenodd"></path>
                    <path fillRule="evenodd" d="M8.5 14a5.5 5.5 0 100-11 5.5 5.5 0 000 11zM15 8.5a6.5 6.5 0 11-13 0 6.5 6.5 0 0113 0z" clipRule="evenodd"></path>
                </svg>
                <Autocomplete
                    ref={this.autocomplete}
                    inputProps={inputProps}
                    wrapperStyle={wrapperStyle}
                    items={stockSearchResults}
                    getItemValue={this.getItemValue}
                    renderItem={this.renderItem}
                    value={this.state.value}
                    onSelect={(value, item) => {
                        this.setState({ value });
                        this.props.selectStock(item);
                    }}
                    onChange={(_, value) => {
                        this.setState({ value });
                        this.onChangeHandler(value);
                    }}
                />
                {
                    this.state.value &&
                    <a className="ml-2" href="#" onClick={() => {
                        this.setState({value: ''});
                        this.props.selectStock({});
                    }}>
                        Clear
                    </a>
                }
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