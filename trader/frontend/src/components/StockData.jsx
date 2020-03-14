import React from 'react';
import PropTypes from 'prop-types';

import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { getStockInfo } from 'actions';

import StockHistoricalData from './StockHistoricalData';
import { formatLargeNumber, formatCurrency } from 'utils';

const mapStateToProps = (state) => {
    return {
        isRequestingStockInfo: state.isRequestingStockInfo,
        stockInfo: state.stockInfo
    };
};

class StockData extends React.Component {

    constructor(props){
        super(props);
    }

    componentDidMount(){
        this.props.getStockInfo(this.props.symbol, 5);
    }

    render(){
        const { stockInfo } = this.props;
        if(!stockInfo){
            return <div/>
        }

        console.log(stockInfo);

        return (
            <div className="row stock-info">
                <div className="col-sm">
                    <div className="stock-header">
                        <div className="stock-symbol">
                            <h5>
                                {stockInfo.data['name']}
                                <span className="badge badge-info stock-badge ml-2">{stockInfo.data['symbol']}</span>
                            </h5>
                            <small>{stockInfo.data['stock_exchange_long']}</small>
                        </div>
                        <div className="stock-price">
                            <h3>
                                {stockInfo.data['price']}
                            </h3>
                        </div>
                    </div>
                    <table className="table stock-info-grid">
                        <tbody>
                            <tr>
                                <th className="stock-info-label" scope="row">Previous Close</th>
                                <td>{formatCurrency(stockInfo.data['close_yesterday'])}</td>
                                <th className="stock-info-label" scope="row">Open</th>
                                <td>{formatCurrency(stockInfo.data['price_open'])}</td>
                            </tr>
                            <tr>
                                <th className="stock-info-label" scope="row">Day's Range</th>
                                <td>{formatCurrency(stockInfo.data['day_low'])} - {formatCurrency(stockInfo.data['day_high'])}</td>
                                <th className="stock-info-label" scope="row">52 Week Range</th>
                                <td>{formatCurrency(stockInfo.data['52_week_low'])} - {formatCurrency(stockInfo.data['52_week_high'])}</td>
                            </tr>
                            <tr>
                                <th className="stock-info-label" scope="row">Volume</th>
                                <td>{formatLargeNumber(stockInfo.data['volume'])}</td>
                                <th className="stock-info-label" scope="row">Avg. Volume</th>
                                <td>{formatLargeNumber(stockInfo.data['volume_avg'])}</td>
                            </tr>
                            <tr>
                                <th className="stock-info-label" scope="row">Market Cap</th>
                                <td>{formatCurrency(stockInfo.data['market_cap'])}</td>
                                <th className="stock-info-label" scope="row">Shares Outstanding</th>
                                <td>{formatLargeNumber(stockInfo.data['shares'])}</td>
                            </tr>
                            <tr>
                                <th className="stock-info-label" scope="row">EPS</th>
                                <td>{formatCurrency(stockInfo.data['eps'])}</td>
                                <th className="stock-info-label" scope="row">P/E Ratio</th>
                                <td>{stockInfo.data['pe']}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div className="col-sm">
                    <StockHistoricalData stockInfo={stockInfo}/>
                </div>
            </div>
        );
    }
}

StockData.propTypes = {
    symbol: PropTypes.string
}

const mapDispatchToProps = (dispatch) => {
    return bindActionCreators(
        { getStockInfo },
        dispatch
    );
}

export default connect(mapStateToProps, mapDispatchToProps)(StockData);