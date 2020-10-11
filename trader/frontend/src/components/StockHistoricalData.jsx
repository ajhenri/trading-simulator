import React from 'react';
import PropTypes from 'prop-types';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { ResponsiveLine } from '@nivo/line';
import Tabs from 'react-bootstrap/Tabs';

import { getStockInfo } from 'actions';
import { formatLargeNumber, formatCurrency } from 'utils';

var moment = require('moment');

const mapStateToProps = (state) => {
    return {
        isRequestingStockInfo: state.isRequestingStockInfo
    };
};

class StockHistoricalData extends React.Component {

    constructor(props){
        super(props);
    }

    render(){
        const { symbol, stockChart, stockQuote } = this.props;

        if(!stockChart){
            return <div/>
        }

        let dataPoints = [];
        for(const i in stockChart){
            dataPoints.push({
                'x': moment(stockChart[i].date),
                'y': stockChart[i].close
            });
        }
        dataPoints.sort((a, b) => {
            return a['x'].unix() - b['x'].unix();
        });

        for(let i=0; i<dataPoints.length; i++){
            dataPoints[i]['x'] = dataPoints[i]['x'].format('MMM Do');
        }

        // Show only the last 5 days for now.
        dataPoints = dataPoints.slice(-5);
        const data = [{ "id": symbol, "data": dataPoints }];

        return (
            <div className="stock-chart" style={{height: 320}}>
                <ResponsiveLine
                    data={data}
                    margin={{ top: 40, right: 50, bottom: 60, left: 60 }}
                    xScale={{ type: 'point' }}
                    yScale={{ type: 'linear', min: 'auto', max: 'auto', stacked: true, reverse: false }}
                    axisTop={null}
                    axisRight={null}
                    axisBottom={{
                        orient: 'bottom',
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                        legend: 'Day',
                        legendOffset: 35,
                        legendPosition: 'middle'
                    }}
                    axisLeft={{
                        orient: 'left',
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                        legend: 'Price',
                        legendOffset: -55,
                        legendPosition: 'middle'
                    }}
                    colors={{ scheme: 'red_yellow_green' }}
                    pointSize={5}
                    pointColor={{ theme: 'background' }}
                    pointBorderWidth={2}
                    pointBorderColor={{ from: 'serieColor' }}
                    pointLabel="y"
                    pointLabelYOffset={-12}
                    crosshairType="cross"
                    theme={{
                        fontFamily: '"Courier New", Courier, monospace',
                        fontSize: 14
                    }}
                    useMesh={true}
                />
            </div>
        );
    }
}

StockHistoricalData.propTypes = {
    symbol: PropTypes.string,
    stockChart: PropTypes.array,
    stockQuote: PropTypes.object
}

const mapDispatchToProps = (dispatch) => {
    return bindActionCreators(
        { getStockInfo },
        dispatch
    );
}

export default connect(mapStateToProps, mapDispatchToProps)(StockHistoricalData);