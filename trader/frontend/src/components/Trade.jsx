import React from 'react';
import PropTypes from 'prop-types';
import Row from 'react-bootstrap/Row';

import { connect } from 'react-redux';
import StockData from './StockData';

import 'css/trade.css';

const mapStateToProps = (state) => {
    return {
        selectedStockSymbol: state.selectedStockSymbol
    };
};

class Trade extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidMount(){
        const { selectedStockSymbol } = this.props;
        if(!selectedStockSymbol){
            let url = new URL(location.href);
            let quote = url.searchParams.get('quote');
            if(quote){
                this.props.setStockSymbol(quote);
            }
        }
    }

    render() {
        const { selectedStockSymbol } = this.props;
        
        return (
            <div>
                {selectedStockSymbol && <StockData symbol={selectedStockSymbol}/>}
            </div>
        );
    }
}

Trade.propTypes = {
    selectedStockSymbol: PropTypes.string
};

export default connect(mapStateToProps)(Trade);