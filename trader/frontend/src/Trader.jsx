import React from 'react';
import PropTypes from 'prop-types';
import { Provider } from 'react-redux';
import configureStore from './store';

import Main from 'components/Main';

const store = configureStore();

class Trader extends React.Component {
    render() {
        return (
            <Provider store={store}>
                <Main/>
            </Provider>
        )
    };
}

export default Trader;