import React from 'react';
import StockData from './StockData';
import StockSearch from './StockSearch';

import 'css/trade.css';

class Trade extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            selectedStock: null
        }

        this.selectStock = this.selectStock.bind(this);
    }

    selectStock(stock){
        this.setState({ selectedStock: stock.symbol })
    }

    render() {
        const { selectedStock } = this.state;
        
        return (
            <div className="row section-body">
                <div className="col-sm">
                    <StockSearch selectStock={this.selectStock} />
                    {selectedStock && <StockData symbol={selectedStock}/>}
                </div>
            </div>
        );
    }
}

export default Trade;