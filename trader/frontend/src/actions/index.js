import axios from 'axios';
import { createDispatchActions } from 'utils';

// #TODO: Configurable Base URL
export const baseURL = 'http://0.0.0.0:5000/api';

export const CREATE_ACCOUNT = createDispatchActions('CREATE_ACCOUNT');
export const GET_ACCOUNT_INFO = createDispatchActions('GET_ACCOUNT_INFO');
export const SEARCH_STOCKS = createDispatchActions('SEARCH_STOCKS');
export const GET_STOCK_INFO = createDispatchActions('GET_STOCK_INFO');
export const SET_STOCK_SYMBOL = 'SET_STOCK_SYMBOL';
export const BUY_STOCK = createDispatchActions('BUY_STOCK');

export function createAccount(data){
    return dispatch => {
        dispatch({
            type: CREATE_ACCOUNT.REQUEST
        });

        axios.post(`${baseURL}/accounts`, data).then((response) => {
            dispatch({
                type: CREATE_ACCOUNT.SUCCESS,
                data: response.data
            });
        }).catch((error) => {
            dispatch({
                type: CREATE_ACCOUNT.ERROR,
                data: error.response
            });
        });
    };
}

export function getAccountInfo(){
    return dispatch => {
        dispatch({
            type: GET_ACCOUNT_INFO.REQUEST
        });

        axios.get(`${baseURL}/accounts`).then((response) => {
            dispatch({
                type: GET_ACCOUNT_INFO.SUCCESS,
                data: response.data
            });
        }).catch((error) => {
            dispatch({
                type: GET_ACCOUNT_INFO.ERROR,
                data: error.response
            });
        });
    };
}

export function searchStocks(symbol){
    return dispatch => {
        dispatch({
            type: SEARCH_STOCKS.REQUEST
        });

        axios.get(`${baseURL}/exchange/search/${symbol}`).then((response) => {
            dispatch({
                type: SEARCH_STOCKS.SUCCESS,
                data: response.data
            });
        }).catch((error) => {
            dispatch({
                type: SEARCH_STOCKS.ERROR,
                data: error.response
            });
        });
    };
}

export function setStockSymbol(symbol){
    return dispatch => {
        dispatch({
            type: SET_STOCK_SYMBOL,
            data: symbol
        });
    };
}

export function getStockInfo(symbol, days){
    return dispatch => {
        dispatch({
            type: GET_STOCK_INFO.REQUEST
        });

        axios.get(`${baseURL}/exchange/history/${symbol}?days=${days}`).then((response) => {
            dispatch({
                type: GET_STOCK_INFO.SUCCESS,
                data: response.data
            });
        }).catch((error) => {
            dispatch({
                type: GET_STOCK_INFO.ERROR,
                data: error.response
            });
        });
    };
}

export function buyStock(account_id, symbol, shares, price){
    return dispatch => {
        dispatch({
            type: BUY_STOCK.REQUEST
        });

        axios.post(`${baseURL}/accounts/${account_id}/stocks`, {
            'symbol': symbol,
            'shares': shares,
            'price': price
        }).then((response) => {
            dispatch({
                type: BUY_STOCK.SUCCESS,
                data: response.data
            });
        }).catch((error) => {
            dispatch({
                type: BUY_STOCK.ERROR,
                data: error.response
            });
        });
    };
}