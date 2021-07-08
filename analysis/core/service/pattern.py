# coding: utf-8

# In[1]:

# bollinger bands is a simple indicator
# just moving average plus moving standard deviation
# but pattern recognition is a different case
# visualization is easy for human to identify the pattern
# but for the machines, we gotta find a different approach
# when we talk about pattern recognition these days
# people always respond with machine learning
# why machine learning when u can use arithmetic approach
# which is much faster and simpler?

# there are many patterns for recognition
# top m, bottom w, head-shoulder top, head-shoulder bottom, elliott waves
# in this content, we only discuss bottom w
# top m is just the reverse of bottom w
# rules of bollinger bands and bottom w can be found in the following link:
# https://www.tradingview.com/wiki/Bollinger_Bands_(BB)

import os
import pandas as pd
import plotly
import plotly.express as px
import copy
import numpy as np
from pandas import DataFrame

# In[2]:
# os.chdir(os.path.dirname(__file__))
# In[3]:

# first step is to calculate moving average and moving standard deviation
# we plus/minus two standard deviations on moving average
# we get our upper, mid, lower bands
from analysis.core.constant.fund_data import FundData
from analysis.lib.utils import get_path


def bollinger_bands(df):
    data = copy.deepcopy(df)
    std = data['price'].rolling(window=20, min_periods=20).std()
    mid_band = data['price'].rolling(window=20, min_periods=20).mean()
    upper_band = mid_band + 2 * std
    lower_band = mid_band - 2 * std
    data['std'] = data['price'].rolling(window=20, min_periods=20).std()
    data['mid band'] = data['price'].rolling(window=20, min_periods=20).mean()
    data['upper band'] = data['mid band'] + 2 * data['std']
    data['lower band'] = data['mid band'] - 2 * data['std']

    return data


# In[4]:


# the signal generation is a bit tricky
# there are four conditions to satisfy
# for the shape of w, there are five nodes
# from left to right, top to bottom, l,k,j,m,i
# when we generate signals
# the iteration node is the top right node i, condition 4
# first, we find the middle node j, condition 2
# next, we identify the first bottom node k, condition 1
# after that, we point out the first top node l
# l is not any of those four conditions
# we just use it for pattern visualization
# finally, we locate the second bottom node m, condition 3
# plz refer to the following link for my poor visualization
# https://github.com/je-suis-tm/quant-trading/blob/master/preview/bollinger%20bands%20bottom%20w%20pattern.png
def signal_generation(data, method):
    # according to investopedia
    # for a double bottom pattern
    # we should use 3-month horizon which is 75
    period = 75

    # alpha denotes the difference between price and bollinger bands
    # if alpha is too small, its unlikely to trigger a signal
    # if alpha is too large, its too easy to trigger a signal
    # which gives us a higher probability to lose money
    # beta denotes the scale of bandwidth
    # when bandwidth is larger than beta, it is expansion period
    # when bandwidth is smaller than beta, it is contraction period
    alpha = 0.0001
    beta = 0.0001

    df = method(data)
    df['signals'] = 0

    # as usual, cumsum denotes the holding position
    # coordinates store five nodes of w shape
    # later we would use these coordinates to draw a w shape
    df['cumsum'] = 0
    df['coordinates'] = ''

    for i in range(period, len(df)):

        # moveon is a process control
        # if moveon==true, we move on to verify the next condition
        # if false, we move on to the next iteration
        # threshold denotes the value of node k
        # we would use it for the comparison with node m
        # plz refer to condition 3
        moveon = False
        threshold = 0.0

        # bottom w pattern recognition
        # there is another signal generation method called walking the bands
        # i personally think its too late for following the trend
        # after confirmation of several breakthroughs
        # maybe its good for stop and reverse
        # condition 4
        if (df['price'][i] > df['upper band'][i]) and \
                (df['cumsum'][i] == 0):

            for j in range(i, i - period, -1):

                # condition 2
                if (np.abs(df['mid band'][j] - df['price'][j]) < alpha) and \
                        (np.abs(df['mid band'][j] - df['upper band'][i]) < alpha):
                    moveon = True
                    break

            if moveon:
                moveon = False
                for k in range(j, i - period, -1):

                    # condition 1
                    if np.abs(df['lower band'][k] - df['price'][k]) < alpha:
                        threshold = df['price'][k]
                        moveon = True
                        break

            if moveon:
                moveon = False
                for l in range(k, i - period, -1):

                    # this one is for plotting w shape
                    if df['mid band'][l] < df['price'][l]:
                        moveon = True
                        break

            if moveon:
                moveon = False
                for m in range(i, j, -1):

                    # condition 3
                    if (df['price'][m] - df['lower band'][m] < alpha) and \
                            (df['price'][m] > df['lower band'][m]) and \
                            (df['price'][m] < threshold):
                        df.at[i, 'signals'] = 1
                        df.at[i, 'coordinates'] = '%s,%s,%s,%s,%s' % (l, k, j, m, i)
                        df['cumsum'] = df['signals'].cumsum()
                        moveon = True
                        break

        # clear our positions when there is contraction on bollinger bands
        # contraction on the bandwidth is easy to understand
        # when price momentum exists, the price would move dramatically for either direction
        # which greatly increases the standard deviation
        # when the momentum vanishes, we clear our positions

        # note that we put moveon in the condition
        # just in case our signal generation time is contraction period
        # but we don't wanna clear positions right now
        if (df['cumsum'][i] != 0) and (df['std'][i] < beta) and (moveon is False):
            df.at[i, 'signals'] = -1
            df['cumsum'] = df['signals'].cumsum()

    return df


# In[5]:
# visualization
def plot(new: DataFrame, code: str):
    # as usual we could cut the dataframe into a small slice
    # for a tight and neat figure
    # a and b denotes entry and exit of a trade
    new.drop(new.head(19).index, inplace=True)
    new.to_csv(get_path('../data/raw/_{}_bb.csv'.format(code)), index=False, sep=',')

    fund_name = FundData.fund_name_df.loc[FundData.fund_name_df['基金代码'] == code, '基金简称'].values[0]
    new = new.drop(labels=['signals', 'cumsum', 'coordinates', 'std'], axis=1, inplace=False)
    fig = px.line(new, x="date", y=new.columns, hover_data={"date": "|%Y-%m-%d"})
    # fig.show()
    fig.update_layout(
        title='{}({})'.format(fund_name, code),
        xaxis_title="日期",
        yaxis_title="累计净值",
        font=dict(
            family="微软雅黑",
            size=16,
            color="#119DFF"
        )
    )
    fig.write_image(get_path('../data/image/bb/{}-{}.png'.format(fund_name, code)))
    # don't show but save as offline .HTML file
    plotly.offline.plot(fig, filename=get_path('../data/html/bb/{}-{}.html'.format(fund_name, code)), auto_open=False)


# In[6]:

# ta-da
def get_bb_data(code):
    """get bollinger bands data for fund with code"""
    # and i take the average of bid and ask price
    df = pd.read_csv(get_path('../data/raw/_{}.csv'.format(code)))
    # fund_em_value_estimation_df = pd.read_csv('../data/raw/fund_em_value_estimation_df.csv')
    # estimation_line = fund_em_value_estimation_df.loc[fund_em_value_estimation_df['基金代码'] == code]
    # if estimation_line is not None:
    #     df
    df.rename(columns={'净值日期': 'date'}, inplace=True)
    df.rename(columns={'累计净值': 'price'}, inplace=True)
    # df = pd.read_csv('h-{}.csv'.format(code))
    # df = df.drop(columns=['open', 'high', 'low', 'volume', 'outstanding_share', 'turnover'])
    signals = signal_generation(df, bollinger_bands)

    new = copy.deepcopy(signals)
    plot(new, code)


def get_multiple_bb_data(code_list):
    """get bollinger bands data for fund in code_list"""
    for code in code_list:
        get_bb_data(code)

