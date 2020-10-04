import React from 'react';
import PropTypes from 'prop-types';

import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { getStockInfo } from 'actions';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';

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

    render(){
        const { stockInfo, accountInfo } = this.props;
        if(!stockInfo) return (<div/>);

        let hasPosition = false;
        for(const [pos, val] of Object.entries(accountInfo.stocks)){
            if(pos == stockInfo.data['symbol']){
                hasPosition = true;
            }
        }

        return (
            <Row>
                <Col>
                    <div className="stock-header">
                        <div className="stock-symbol float-left">
                            <h5>
                                {stockInfo.data['name']}
                                <span className="badge badge-info stock-badge ml-2">{stockInfo.data['symbol']}</span>
                            </h5>
                            <small>{stockInfo.data['stock_exchange_long']}</small>
                        </div>
                        <div className="stock-price float-right">
                            <h3>
                                ${stockInfo.data['price']}
                            </h3>
                        </div>
                        <div className="clearfix"></div>
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
                    <div className="ml-2 mt-2">
                        <Button className="mr-1" size="sm" onClick={() => this.props.showModal('buy', true)}>
                            Buy
                        </Button>
                        <Button className="mr-1" size="sm" onClick={() => this.props.showModal('sell', true)} disabled={!hasPosition}>
                            Sell
                        </Button>
                        <Button className="mr-1" size="sm" onClick={() => this.props.showModal('sell', true)} disabled={!hasPosition}>
                            Sell All
                        </Button>
                    </div>
                </Col>
                <Col>
                    <StockHistoricalData stockInfo={stockInfo}/>
                </Col>
            </Row>
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