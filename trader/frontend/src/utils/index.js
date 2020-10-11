export function isEmpty(str) {
    return (!str || 0 === str.length);
}

export function formatError(error) {
    if(error instanceof String) return error;

    let formattedError = {};
    for(let k in error){
        if(error[k] instanceof Array){
            formattedError[k] = error[k][0];
        } else {
            formattedError[k] = error[k];
        }
    }

    return formattedError;
}

export const createDispatchActions = (action) => {
    return {
        REQUEST: `${action}_REQUEST`,
        SUCCESS: `${action}_SUCCESS`,
        ERROR: `${action}_ERROR`
    };
};

export const TRILLION = 1000000000000;
export const BILLION = 1000000000;
export const MILLION = 1000000;

export const formatLargeNumber = (num) => {
    if(num >= TRILLION){
        return (num/TRILLION).toFixed(2) + 'T';
    }
    else if(num >= BILLION){
        return (num/BILLION).toFixed(2) + 'B';
    }
    else if(num >= MILLION){
        return (num/MILLION).toFixed(2) + 'M';
    }
    return num;
}

export const formatCurrency = (currency) => {
    const formatter = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });
    if(currency >= MILLION){
        return '$' + formatLargeNumber(currency);
    }
    return formatter.format(currency);
};