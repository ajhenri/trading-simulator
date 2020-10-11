import React from 'react';
import PropTypes from 'prop-types';

import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { getStockInfo } from 'actions';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';

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
        if(!stockInfo[this.props.symbol]) return (<div/>);

        let hasPosition = false;
        for(const [pos, _] of Object.entries(accountInfo.stocks)){
            if(pos == stockInfo[this.props.symbol]['quote']['symbol']){
                hasPosition = true;
            }
        }

        const quote = stockInfo[this.props.symbol]['quote'];
        const chart = stockInfo[this.props.symbol]['chart'];

        return (
            <Row>
                <Col>
                    <div className="stock-header">
                        <div className="stock-symbol float-left">
                            <h5>
                                {quote.companyName}
                                <span className="badge badge-info stock-badge ml-2">{quote.symbol}</span>
                            </h5>
                            <small>{quote.primaryExchange}</small>
                        </div>
                        <div className="stock-price float-right">
                            <h3>
                                ${quote.latestPrice}
                            </h3>
                        </div>
                        <div className="clearfix"></div>
                    </div>
                    <table className="table stock-info-grid">
                        <tbody>
                            <tr>
                                <th className="stock-info-label" scope="row">Previous Close</th>
                                <td>{formatCurrency(quote.previousClose)}</td>
                                <th className="stock-info-label" scope="row">Open</th>
                                <td>{formatCurrency(quote.open)}</td>
                            </tr>
                            <tr>
                                <th className="stock-info-label" scope="row">Day's Range</th>
                                <td>{formatCurrency(quote.low)} - {formatCurrency(quote.high)}</td>
                                <th className="stock-info-label" scope="row">52 Week Range</th>
                                <td>{formatCurrency(quote.week52Low)} - {formatCurrency(quote.week52High)}</td>
                            </tr>
                            <tr>
                                <th className="stock-info-label" scope="row">Volume</th>
                                <td>{formatLargeNumber(quote.volume)}</td>
                                <th className="stock-info-label" scope="row">Avg. Volume</th>
                                <td>{formatLargeNumber(quote.avgTotalVolume)}</td>
                            </tr>
                            <tr>
                                <th className="stock-info-label" scope="row">Market Cap</th>
                                <td>{formatCurrency(quote.marketCap)}</td>
                            </tr>
                            <tr>
                                <th className="stock-info-label" scope="row">EPS</th>
                                <td>EPS</td>
                                <th className="stock-info-label" scope="row">P/E Ratio</th>
                                <td>{quote.peRatio}</td>
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
                    <StockHistoricalData symbol={this.props.symbol} stockQuote={quote} stockChart={chart}/>
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