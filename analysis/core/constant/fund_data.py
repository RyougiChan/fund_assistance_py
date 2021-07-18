import os

import pandas as pd

from analysis.lib.utils import get_path


class FundData:
    fund_em_fund_name_df_path = get_path('data/raw/fund_em_fund_name_df.csv')
    fund_name_df = pd.read_csv(fund_em_fund_name_df_path, dtype={'基金代码': str}) \
        if os.path.exists(fund_em_fund_name_df_path) \
        else None


