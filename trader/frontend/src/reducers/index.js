import {
    CREATE_ACCOUNT,
    GET_ACCOUNT_INFO,
    SEARCH_STOCKS,
    GET_STOCK_INFO,
    SET_STOCK_SYMBOL,
    BUY_STOCK
} from 'actions';

const INITIAL_STATE = {};

const rootReducer = (state = INITIAL_STATE, action) => {
    console.log(state);
    console.log(action);
    switch(action.type){
        case CREATE_ACCOUNT.REQUEST:
            return {
                ...state,
                isCreatingAccount: true
            };
        case CREATE_ACCOUNT.SUCCESS:
            return {
                ...state,
                isCreatingAccount: false,
                account: action.data
            };
        case CREATE_ACCOUNT.ERROR:
            return {
                ...state,
                isCreatingAccount: false,
                createAccountError: action.data
            };
        case GET_ACCOUNT_INFO.REQUEST:
            return {
                ...state,
                isRequestingAccountInfo: true
            };
        case GET_ACCOUNT_INFO.SUCCESS:
            return {
                ...state,
                isRequestingAccountInfo: false,
                accountInfo: action.data.result
            };
        case GET_ACCOUNT_INFO.ERROR:
            return {
                ...state,
                isRequestingAccountInfo: false,
                accountInfoError: action.data
            };
        case SEARCH_STOCKS.REQUEST:
            return {
                ...state,
                isRequestingStockSearch: true
            };
        case SEARCH_STOCKS.SUCCESS:
            return {
                ...state,
                isRequestingStockSearch: false,
                stockSearchResults: action.data.result
            };
        case SEARCH_STOCKS.ERROR:
            return {
                ...state,
                isRequestingStockSearch: false,
                stockSearchError: action.data
            };
        case GET_STOCK_INFO.REQUEST:
            return {
                ...state,
                isRequestingStockInfo: true
            };
        case GET_STOCK_INFO.SUCCESS:
            return {
                ...state,
                isRequestingStockInfo: false,
                stockInfo: action.data.result
            };
        case GET_STOCK_INFO.ERROR:
            return {
                ...state,
                isRequestingStockInfo: false,
                stockInfoError: action.data
            };
        case SET_STOCK_SYMBOL:
            return {
                ...state,
                selectedStockSymbol: action.data
            };
        case BUY_STOCK.REQUEST:
            return {
                ...state,
                isTradingStock: true
            };
        case BUY_STOCK.SUCCESS:
            return {
                ...state,
                isTradingStock: false,
                buyStockResult: action.data
            };
        case BUY_STOCK.ERROR:
            return {
                ...state,
                isTradingStock: false,
                buyStockError: action.data
            };
        default:
            return state;
    }
};

export default rootReducer;