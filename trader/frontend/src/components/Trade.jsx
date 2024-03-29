import React from 'react';
import PropTypes from 'prop-types';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { getAccountInfo, getStockInfo, buyNewStock, tradeExistingStock } from 'actions';
import Dialog from './Dialog';
import StockData from './StockData';

import 'css/trade.css';

const Loader = require('react-loader');
const mapStateToProps = (state) => {
    return {
        isRequestingAccountInfo: state.isRequestingAccountInfo,
        isTradingStock: state.isTradingStock,
        accountInfoError: state.accountInfoError,
        accountInfo: state.accountInfo,
        selectedStockSymbol: state.selectedStockSymbol,
        stockInfo: state.stockInfo
    };
};

class Trade extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            modals: {
                buy: {
                    show: false
                },
                sell: {
                    show: false,
                    sellAll: false
                }
            },
            numberOfShares: 1
        }

        this.buyStock = this.buyStock.bind(this);
        this.sellStock = this.sellStock.bind(this);
        this.showModal = this.showModal.bind(this);
        this.handleFieldChange = this.handleFieldChange.bind(this);
    }

    componentDidMount(){
        const { selectedStockSymbol } = this.props;
        if(!selectedStockSymbol){
            let url = new URL(location.href);
            let quote = url.searchParams.get('quote');
            if(quote){
                this.props.setStockSymbol(quote);
                this.props.getStockInfo(quote);
            }
        }
        this.props.getAccountInfo();
    }

    showModal(modalName, show){
        let modals = this.state.modals;

        let numberOfShares = 1;
        let sellAll = false;
        if(modalName == 'sellAll'){
            sellAll = true;
            modalName = 'sell';

            const { selectedStockSymbol, accountInfo } = this.props;
            numberOfShares = accountInfo.stocks[selectedStockSymbol].shares;
        }
        if (modals[modalName]){
            modals[modalName].show = show;
            if(modalName == 'sell'){
                modals[modalName].sellAll = sellAll;
            }
            this.setState({
                modals: modals,
                numberOfShares: numberOfShares
            });
        }
    }

    handleFieldChange(event){
        let state = this.state;
        if(event.target && event.target.name){
            state[event.target.name] = event.target.value;
            this.setState(state);
        }
    }

    buyStock(){
        const { stockInfo, selectedStockSymbol, accountInfo } = this.props;
        const hasStock = accountInfo.stocks && accountInfo.stocks[selectedStockSymbol];
        const stockQuote = stockInfo[selectedStockSymbol]['quote'];
        if(!hasStock){
            this.props.buyNewStock(accountInfo.id, selectedStockSymbol, this.state.numberOfShares, stockQuote.latestPrice);
        } else {
            const stock = accountInfo.stocks[selectedStockSymbol];
            this.props.tradeExistingStock(accountInfo.id, stock.id, {
                'symbol': selectedStockSymbol,
                'shares': this.state.numberOfShares,
                'price': stockQuote.latestPrice,
                'trade_type': 'buy'
            })
        }
    }

    sellStock(){
        const { stockInfo, selectedStockSymbol, accountInfo } = this.props;
        const stock = accountInfo.stocks[selectedStockSymbol];
        const stockQuote = stockInfo[selectedStockSymbol]['quote'];
        this.props.tradeExistingStock(accountInfo.id, stock.id, {
            'symbol': selectedStockSymbol,
            'shares': this.state.numberOfShares,
            'price': stockQuote.latestPrice,
            'trade_type': 'sell'
        });
    }

    render() {
        const { modals } = this.state;
        const { selectedStockSymbol, stockInfo, accountInfo } = this.props;

        if(!accountInfo || !stockInfo || !stockInfo[selectedStockSymbol]) return (<div/>);
        const s = stockInfo[selectedStockSymbol];
        const maximumShares = Math.floor(parseFloat(accountInfo.cash_amount)/parseFloat(s['quote']['latestPrice']));
        const sharesOwned = accountInfo.stocks && accountInfo.stocks[selectedStockSymbol] ? 
            accountInfo.stocks[selectedStockSymbol].shares : 0;

        return (
            <div>
                {   selectedStockSymbol && 
                    <StockData 
                        symbol={selectedStockSymbol} 
                        stockInfo={stockInfo} showModal={this.showModal}
                        accountInfo={accountInfo}
                    />
                }
                <Dialog 
                    title={"Buy Position"}
                    show={modals.buy.show}
                    submitText={'Buy'}
                    onSubmit={this.buyStock}
                    hideModal={() => this.showModal('buy', false)}
                >
                    <Form>
                        <p>How many shares of <strong>{selectedStockSymbol}</strong> do you want to buy?</p>
                        <Form.Group>
                            <Form.Control 
                                type="number" name="numberOfShares"
                                placeholder="Shares" min={1} max={maximumShares} 
                                value={this.state.numberOfShares}
                                onChange={this.handleFieldChange}
                            />
                        </Form.Group>
                        <small>Maximum Shares: {maximumShares}</small>
                    </Form>
                </Dialog>
                <Dialog 
                    title={"Sell Position"}
                    show={modals.sell.show}
                    submitText={'Sell'}
                    onSubmit={this.sellStock}
                    hideModal={() => this.showModal('sell', false)}
                >
                    <Form>
                        <p>How many shares of <strong>{selectedStockSymbol}</strong> do you want to sell?</p>
                        <Form.Group>
                            <Form.Control 
                                type="number" name="numberOfShares" 
                                placeholder="Shares" min={1} max={sharesOwned} 
                                value={this.state.numberOfShares}
                                onChange={this.handleFieldChange}
                            />
                            {sharesOwned > 0 && <p>Shares Owned: {sharesOwned}</p>}
                        </Form.Group>
                    </Form>
                    <small></small>
                </Dialog>
                <Loader loaded={!this.props.isTradingStock} className="spinner" />
            </div>
        );
    }
}

Trade.propTypes = {
    selectedStockSymbol: PropTypes.string,
    stockInfo: PropTypes.object,
    accountInfo: PropTypes.object
};

const mapDispatchToProps = (dispatch) => {
    return bindActionCreators(
        { getAccountInfo, getStockInfo, buyNewStock, tradeExistingStock },
        dispatch
    );
}

export default connect(mapStateToProps, mapDispatchToProps)(Trade);