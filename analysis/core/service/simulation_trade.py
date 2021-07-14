from threading import Thread

import pandas as pd
import plotly
import plotly.graph_objs as go

from datetime import datetime
from dateutil.relativedelta import relativedelta
from analysis.conf.yconfig import YConfig
from analysis.core.constant.fund_data import FundData
from analysis.core.service.aliyun_oss import AliyunOss
from analysis.core.service.fund import get_daily_operation_by_bb, get_buy_amount_by_bb
from analysis.lib.utils import get_path, absolute_file_paths


class SimulationTrade:
    init_balance = 0
    start_money = 0
    max_used_money = 0
    max_draw_down = 0
    start_trade_date = None

    @staticmethod
    def init():
        stp = YConfig.get('simulation_trade_params')
        SimulationTrade.init_balance = stp['init_balance']
        SimulationTrade.start_money = stp['start_money']
        SimulationTrade.start_trade_date = datetime.fromisoformat(stp['start_trade_date'])

    @staticmethod
    def start_simulation_trade(code):
        return SimulationTrade.start_multiple_simulation_trade([code])

    @staticmethod
    def start_multiple_simulation_trade(code_list: list):
        cash = SimulationTrade.init_balance
        process = 0
        now = datetime.now()
        max_used_money = 0
        initial_fund_capital = SimulationTrade.start_money * len(code_list)
        initial_capital = cash + initial_fund_capital
        max_daily_money = initial_capital
        min_daily_money = initial_capital
        daily_money_df = [[], []]
        depot = dict()
        fund_em_info = dict()

        for code in code_list:
            # 获取累计净值
            fund_em_info_df_total_net_worth = pd.read_csv(get_path('data/raw/_' + code + '.csv'))[
                ["净值日期", "累计净值"]]
            fund_em_info.update({code: fund_em_info_df_total_net_worth})
            depot.update({code: SimulationTrade.start_money})
            operation_recorder = dict()
            operation_recorder.update({'日期': []})
            operation_recorder.update({code: []})
            operation_price_recorder = dict()
            operation_price_recorder.update({code: []})
            operation_price_recorder.update({'日期': []})
            operation_price_recorder.update({'color': []})
            trade_date = SimulationTrade.start_trade_date
            while trade_date <= now:
                # 进度记录
                process += 1
                if process == 50:
                    process = 0

                # 周末是非交易日直接跳过
                if trade_date.weekday() == 5 or trade_date.weekday() == 6:
                    trade_date += relativedelta(days=+1)
                    continue

                # 根据布林带判断每日交易(观望，买入，卖出)
                daily_operation = get_daily_operation_by_bb(code, str(trade_date).split(' ')[0])

                # 计算日增长率(不考虑分红)
                df = fund_em_info[code]
                temp_total_worth_data = df.loc[df['净值日期'] == str(trade_date).split(' ')[0]]
                temp_indexes = temp_total_worth_data.index.tolist()
                today_worth = 0
                if len(temp_indexes):
                    temp_index = temp_indexes[0]
                    today_worth = temp_total_worth_data['累计净值'].values[0]
                    last_date_worth = df.iloc[temp_index - 1, 1]
                    inc_rate = (today_worth - last_date_worth) / last_date_worth
                    # 更新前一个交易日收益
                    # if key == '160629':
                    #     print('余额：', depot[key], ' 增长率：', inc_rate, ' 结余：', depot[key] * (1 + inc_rate))
                    depot.update({code: depot[code] * (1 + inc_rate)})

                # 操作记录-日期
                operation_recorder['日期'].append(str(trade_date))
                operation_price_recorder['日期'].append(str(trade_date))
                # 操作记录-操作价格
                operation_price_recorder[code].append(today_worth)

                # 获取每日交易数量(观望 0，买入 +，卖出 -)
                daily_buy_amount = get_buy_amount_by_bb(cash, depot[code], daily_operation)
                color = 'lightblue'
                if daily_buy_amount is not None:
                    if daily_buy_amount > 0:
                        color = 'red'
                    elif daily_buy_amount < 0:
                        color = 'green'
                operation_price_recorder['color'].append(color)
                # 观望直接继续下一个交易日
                if daily_buy_amount is None or cash - daily_buy_amount < 0:
                    operation_recorder[code].append(0)
                    trade_date += relativedelta(days=+1)
                    continue
                # 交易手续费
                trade_fee = daily_buy_amount * 0.0015
                operation_recorder[code].append(daily_buy_amount)
                depot.update({code: depot[code] + daily_buy_amount})
                cash -= (daily_buy_amount + (0 if daily_buy_amount < 0 else trade_fee))
                # 更新最大资金用量
                if cash < max_used_money:
                    max_used_money = cash

                trade_date += relativedelta(days=+1)
                daily_total_money = cash
                daily_total_money += depot[code]
                daily_money_df[0].append(trade_date)
                daily_money_df[1].append(daily_total_money)
                # print(daily_total_money, balance, min_daily_money)
                if daily_total_money > max_daily_money:
                    max_daily_money = daily_total_money
                    min_daily_money = daily_total_money
                if daily_total_money < min_daily_money:
                    min_daily_money = daily_total_money
                if daily_buy_amount is not None:
                    # print('{} 剩余现金：{}'.format(trade_date, cash))

                    ttt = 0
                    for v in depot.values():
                        ttt += v

                    # print('{} 基金持仓：{}'.format(trade_date, ttt))

            # 画图
            df = pd.DataFrame({'日期': daily_money_df[0], '收益': daily_money_df[1]})
            op_df = pd.DataFrame(operation_price_recorder)

            # 基金名称
            fund_name = FundData.fund_name_df.loc[FundData.fund_name_df['基金代码'] == code, '基金简称'].values[0]

            m_fig = go.Figure()
            m_fig.add_trace(
                go.Scatter(
                    name="{}-操作".format(fund_name),
                    mode="markers", x=op_df["日期"], y=op_df[code],
                    text=fund_name,
                    marker={
                        'symbol': 'star',
                        'color': op_df['color']
                    }
                )
            )
            m_fig.update_layout(
                title='{}({})'.format(fund_name, code),
                xaxis_title="日期",
                yaxis_title="累计净值",
                font=dict(
                    family="微软雅黑",
                    size=16,
                    color="#119DFF"
                )
            )
            m_fig.update_xaxes(dtick="M1", tickformat="%d\n%b")
            m_fig.write_image(get_path('data/image/simulation_trade/{}-{}.png'.format(fund_name, code)))
            plotly.offline.plot(m_fig, filename=get_path('data/html/simulation_trade/{}-{}.html'.format(fund_name, code)), auto_open=False)

        t1 = Thread(target=AliyunOss.put_objects,
                    args=('html/simulation_trade/', absolute_file_paths(get_path('data/html/simulation_trade')),))
        t2 = Thread(target=AliyunOss.put_objects,
                    args=('image/simulation_trade/', absolute_file_paths(get_path('data/image/simulation_trade')),))
        t3 = Thread(target=AliyunOss.put_objects,
                    args=('html/bollinger_bands/', absolute_file_paths(get_path('data/html/bollinger_bands')),))
        t4 = Thread(target=AliyunOss.put_objects,
                    args=('image/bollinger_bands/', absolute_file_paths(get_path('data/image/bollinger_bands')),))
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        # 清算
        # 账户结余
        end_total_money = 0
        for v in depot.values():
            end_total_money += v

        earning = end_total_money + cash - initial_capital
        x = initial_fund_capital
        k = end_total_money
        s = end_total_money + cash
        r = earning / initial_capital
        max_draw_down = (max_daily_money - min_daily_money) / max_daily_money
        output = [
            {'初始总资金': initial_capital},
            {'初始基金金额x': x},
            {'最大投入': SimulationTrade.init_balance - max_used_money + x},
            {'剩余流动资金': cash},
            {'最终基金金额': k},
            {'最终账户总金额': s},
            {'收益': earning},
            {'最终账户收益率': r},
            {'最大回撤': max_draw_down},
        ]
        return output
