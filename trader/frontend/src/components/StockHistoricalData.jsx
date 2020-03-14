import React from 'react';
import PropTypes from 'prop-types';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { ResponsiveLine } from '@nivo/line';
import { getStockInfo } from 'actions';
import { formatLargeNumber, formatCurrency } from 'utils';

var moment = require('moment');

const mapStateToProps = (state) => {
    return {
        isRequestingStockInfo: state.isRequestingStockInfo,
        stockInfo: state.stockInfo
    };
};

class StockHistoricalData extends React.Component {

    constructor(props){
        super(props);
    }

    render(){
        const { stockInfo } = this.props;
        if(!stockInfo){
            return <div/>
        }

        let history = stockInfo.history;
        let dataPoints = [];
        for(const day in history){
            dataPoints.push({
                'x': moment(day),
                'y': history[day].open
            });
        }
        dataPoints.sort((a, b) => {
            return a['x'].unix() - b['x'].unix();
        });

        for(let i=0; i<dataPoints.length; i++){
            dataPoints[i]['x'] = dataPoints[i]['x'].format('dddd');
        }

        const data = [{ "id": stockInfo.data['symbol'], "data": dataPoints }];

        console.log(stockInfo);

        return (
            <div className="stock-chart" style={{height: 250}}>
                <ResponsiveLine
                    data={data}
                    margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
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
                        legendOffset: 36,
                        legendPosition: 'middle'
                    }}
                    axisLeft={{
                        orient: 'left',
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                        legend: 'Price',
                        legendOffset: -40,
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
                    useMesh={true}
                />
            </div>
        );
    }
}

StockHistoricalData.propTypes = {
    stockInfo: PropTypes.object
}

const mapDispatchToProps = (dispatch) => {
    return bindActionCreators(
        { getStockInfo },
        dispatch
    );
}

export default connect(mapStateToProps, mapDispatchToProps)(StockHistoricalData);