import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
import pytz
import yfinance as yf
yf.pdr_override()
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_datareader import data as pdr


def get_ccy_data(start, end, ccys):
    """
    Args:
        start: datetime object e.g. datetime.datetime.now()
        end: datetime object
        ccys: a list of USD pairs in Yahoo Finance's ticker naming
            convention. E.g. "GBP=X"
            
    Returns:
        df = A dataframe containing hourly close for all the currency 
            pairs supplied
    """
    df_list=[]
    
    for i, c in enumerate(ccys):
        ccy = pdr.get_data_yahoo(
            ccys[i],
            start,
            end,
            interval='60m')['Close'].rename(str(c[:-2]))
        df_list.append(ccy)

    df = pd.concat(df_list, axis=1)
    df = df.reset_index()
    
    # change timezone to NY
    new_timezone = pytz.timezone("America/New_York")
    df['Datetime'] = df.apply(lambda row: row['Datetime']\
                       .astimezone(new_timezone), axis=1)
    df = df.set_index('Datetime')
    
    return df


def overnight_returns(start, end, ccys):
    df = get_ccy_data(start, end, ccys)
    df = df[(df.index.hour == 17) |  (df.index.hour == 5)].pct_change()[-1:]
    return df


def calculate_crosses(df):
    """
    Using the list of USD crosses that already exist in the
    currencies dataframe, this function finds all the possible
    combinations of crosses that can be achieved with those.
    
    Args:
        df: the dataframe output from get_ccy_data

    Returns:
        df_crosses: a dataframe containing exchange rates for all
            possible crosses from the original USD pairs supplied
            in get_ccy_data.
    """
    
    dollar_ccy = list(df.columns) # list of currencies against the dollar

    # get the various combinations of crosses we can make from these
    crosses_tuple = [(dollar_ccy[i],dollar_ccy[j]) 
                         for i in range(len(dollar_ccy))
                             for j in range(i+1, len(dollar_ccy))]

    # calculate them
    for cross in crosses_tuple:
        col_name = str(cross[0]) + "/" + str(cross[1])
        cross1 = cross[0]
        cross2 = cross[1]
        df[col_name] = (1/ (df[cross1] / df[cross2]))
        
    # prepend "USD/" in front of the dollar pairs
    df.columns = ['USD/'+x if len(x) == 3 else x for x in df.columns]
    
    return df


def inverse_currencies(df, currencies):
    """
    Some pairs will be need to be raised to the power of -1 to get
    the desired exchange rate. e.g. USD/EUR -> EUR/USD.
    
    Also removed the "/" in the column names for consistency with
    existing indicators.
    
    Args:
        df: A dataframe containing hourly exchange rates of various
            currency pairs
            
    Returns:
        df_inversed: A dataframe with all the original currencies supplied,
            however the specified currency pairs will have been inversed.
    """
    for col in df.columns:
        if col in currencies:
            df[col] = 1/df[col]
            numerator = col[:3]
            denominator = col[4:]
            df = df.rename(columns={col: denominator+"/"+numerator})
    
    # remove slashes to bring format in line with existing indicators
    df.columns = df.columns.str.replace("/", "")
    
    df_inversed = df.copy()
    
    return df_inversed


def return_bar_data(df, ccy_group):
    """
    Reformats the hourly returns dataframes into to be used in
    a plotly express bar chart.
    
    Args:
        df: dataframe containing hourly returns for all
            the currencies.
        ccy_group: A list of currencies (e.g G10 currencies) in the
            format "EURGBP".
            
    Returns:
        df_bar: A dataframe where 
            index 0 = overnight standard deviation move
            index 1 = overnight return
            index 2 = overnight return (formatted for annotations)
    """
    
    # filter on relevent hours
    
    df = df[
        (df.index.hour == 18) |  (df.index.hour == 6)
    ]
    
    # if the time is later than 9, filter out that row because we are only
    # interested in calculating the differnce overnight
    if df.index[-1].hour > 9:
        df = df.iloc[:-1, :]
            
    on_returns_hist = df.pct_change()
    
    # get most recent o/n return, and 200d stddev 
    on_returns_recent = df.pct_change()[-1:]
    
    std_200d = on_returns_hist.std()
    
    # calculate the size of the move in terms of 200d stddev
    std_dev_move = on_returns_recent / std_200d
    
    # get the values for plotting
    labels = on_returns_recent[ccy_group].columns
    stddev = std_dev_move[ccy_group]
    rtn = on_returns_recent[ccy_group]
    
    df_bar = pd.concat([ stddev, rtn], axis=0).T
    df_bar.columns = ['std_dev_move', 'return']
    
    # sort by first column (std. dev. move)
    df_bar = df_bar.sort_values(by='std_dev_move', ascending=False)
    df_bar = df_bar.T.reset_index(drop=True)
    
    # for annotations
    xcoords = list(np.arange(len(df_bar.columns)))
    stddevs = list(df_bar.iloc[0, :].values) # for annot height
    rtns = ["{0:.2%}".format(x) for x in list(df_bar.iloc[1, :].values)]

    # put into format for px.bar
    df_bar = df_bar.T.reset_index().rename(
        columns={'index': 'pair', 0: 'std_dev_move', 1: 'rtn'})
    
    df_bar['rtn_formatted'] = ["{0:.2%}".format(x) 
                               for x in list(df_bar.iloc[:, 2].values)]    
    
    return df_bar


def return_heatmap_data(dfs, rows, columns):
    """
    Returns the data behind the heatmaps showing the standard deviation
    move and returns.
    
    Args:
        dfs: list of dataframes generated by return_bar_data().
    Returns:
        4 heatmaps
            - All currencies
            - G10
            - Other G10
            - EM vs USD    
    """
    
    # gather the dataframes
    
    dff = pd.concat(dfs, axis=0).sort_values(by="std_dev_move", ascending=False)
    
    # create the all currencies heatmap; e.g. 66 currencies; 6rowx11col matrix
    dff['Xcols'] = list(np.arange(1,columns+1))*rows
    Yrows = []

    for i in np.arange(1, rows+1):
        Yrows += [i]*columns
    dff['Yrows'] = Yrows
    
    symbols = ((np.asarray(dff['pair'])).reshape(rows, columns))
    stddevs = ((np.asarray(dff['std_dev_move'])).reshape(rows, columns))
    rtns = ((np.asarray(dff['rtn_formatted'])).reshape(rows, columns))
    
    table = dff.pivot(index='Yrows', columns='Xcols', values='std_dev_move')
    
    labels = (np.asarray(["{0} \n {1:.2f}σ \n {2}".format(sym, std, rtn)
                          for sym, std, rtn in 
                          zip(symbols.flatten(), stddevs.flatten(), rtns.flatten())
              ])
         ).reshape(rows,columns)
    
    return table, labels


def create_heatmap(table, labels, theme, output_name=None):
    fig, ax = plt.subplots(figsize=(16, 8), dpi=250)

    
    # boolean to indicate which currency groups the boolean contains
    g10_currencies = np.any(np.char.find(labels, "GBPUSD") == 0) # G10 currency found
    otherg10_currencies = np.any(np.char.find(labels, "GBPSEK") == 0) # Other G10 currency found
    em_currencies = np.any(np.char.find(labels, "USDTWD") == 0) # EM currency found
    
    # if labels contain all currency groups
    if np.all([g10_currencies,  otherg10_currencies, em_currencies]):
        group = " - G10 & EM"
    elif g10_currencies == True:
        group =  " - G10 vs USD"
    elif otherg10_currencies == True:
        group = " - Other G10"
    else:
        group = " - EM vs USD"


    title = "Overnight FX Returns"+group
    last_update = datetime.datetime.now().strftime("%d-%b-%Y %H:%M%p")
    
    plt.title(title, fontsize=18)
    ttl = ax.title
    ttl.set_position([0.5, 1.05])

    fig.text(0.13, 0.08, "Last updated: {}".format(last_update), ha ='left', fontsize = 12)

    
    ax.set_xticks([])
    ax.set_yticks([])

    ax.axis('off')

    sns.heatmap(table, annot=labels, fmt="", cmap=theme,
                linewidths=0.30, ax=ax, cbar=False)
    if output_name:
        fig.savefig("recordcurrency/static/images/{}.png".format(output_name))
        fig.savefig("recordcurrency/static/images/{}{}.png".format(output_name, "_new"))
        print("created a new heatmap called:", "recordcurrency/static/images/{}{}.png".format(output_name, "_new"))





ccy = [
    'GBP=X', 'EUR=X', 'NZD=X', 'CHF=X', 'JPY=X', 'AUD=X', 'CAD=X',
    'CZK=X', 'HUF=X', 'ZAR=X',  'MXN=X', 'PLN=X', 'TRY=X', 'RUB=X',
    'BRL=X', 'COP=X', 'CLP=X', 'PEN=X', 'RON=X',  'TWD=X', 'THB=X',
    'IDR=X', 'INR=X', 'HKD=X', 'SGD=X', 'CNH=X', 'CNY=X', 'PHP=X', 
    'MYR=X', 'KRW=X', 'DKK=X', 'SEK=X', 'NOK=X'
]

ccys_to_inverse = [
    'USD/EUR', 'USD/GBP', 'USD/AUD', 'USD/NZD', 'GBP/EUR', 'NZD/AUD',
    'CHF/AUD', 'JPY/AUD', 'CHF/CAD', 'SEK/NOK', 'JPY/NOK', 'JPY/SEK',
    'JPY/CAD'
]

# define currency groups
G10vUSD = [
    'EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF', 'AUDUSD', 'USDCAD',
    'NZDUSD', 'USDNOK', 'USDSEK'
]

otherG10 = [
    'EURGBP', 'EURAUD', 'EURNZD', 'EURCAD', 'EURCHF', 'EURNOK', 
    'EURSEK', 'EURJPY', 'GBPAUD', 'GBPNZD', 'GBPCAD', 'GBPCHF',
    'GBPNOK', 'GBPSEK', 'GBPJPY', 'AUDNZD', 'AUDCAD', 'AUDCHF',
    'AUDNOK', 'AUDSEK', 'AUDJPY', 'NZDCAD', 'NZDCHF', 'NZDNOK',
    'NZDSEK', 'NZDJPY', 'CADCHF', 'CADNOK', 'CADSEK', 'CADJPY',
    'CHFNOK', 'CHFSEK', 'CHFJPY', 'NOKSEK',  'NOKJPY', 'SEKJPY'
    ]

EMvsUSD = [
    'USDBRL', 'USDCLP', 'USDCNH', 'USDCNY', 'USDCOP', 'USDCZK',
    'USDHUF', 'USDIDR', 'USDINR', 'USDKRW', 'USDMXN', 'USDMYR',
    'USDPEN', 'USDPHP', 'USDPLN', 'USDRON', 'USDRUB', 'USDTRY',
    'USDTWD', 'USDZAR', 'USDTHB'
]


if __name__ == "__main__":
    start = datetime.datetime.now() - relativedelta(days=200)
    end = datetime.datetime.now()

    df = get_ccy_data(start, end, ccy).interpolate()
    df = calculate_crosses(df)
    df = inverse_currencies(df=df, currencies=ccys_to_inverse)

    print("Saved dataframe containing historical rates...")

    df_g10 = return_bar_data(df, ccy_group=G10vUSD)
    df_otherg10 = return_bar_data(df, ccy_group=otherG10)
    df_EM = return_bar_data(df, ccy_group=EMvsUSD)

    allccy_table, allccy_labels = return_heatmap_data([df_g10, df_otherg10, df_EM], rows=6, columns=11)
    g10_table, g10_labels = return_heatmap_data([df_g10], rows=3, columns=3)
    otherg10_table, other10_labels = return_heatmap_data([df_otherg10], rows=6, columns=6)
    EM_table, EM_labels = return_heatmap_data([df_EM], rows=3, columns=7)

    print("Transformed the data ready for heatmap...")

    create_heatmap(allccy_table, allccy_labels, theme="RdBu", output_name="ONFXRTN_all")
    create_heatmap(g10_table, g10_labels, theme="RdBu", output_name="ONFXRTN_g10")
    create_heatmap(otherg10_table, other10_labels, theme="RdBu", output_name="ONFXRTN_otherg10")
    create_heatmap(EM_table, EM_labels, theme="RdBu", output_name="ONFXRTN_em")

    print("Saved heatmaps to .pngs")
    print("FINISHED")