import pandas as pd

from analysis.lib.utils import get_path


class FundData:
    fund_name_df = pd.read_csv(get_path('../data/raw/fund_em_fund_name_df.csv'), dtype={'基金代码': str})
