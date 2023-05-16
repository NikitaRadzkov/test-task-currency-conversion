import pandas as pd
from typing import Optional
from api.get_raw_data import get_raw_data
from api.get_exchange_rate import get_exchange_rate
from constants import TIME_PERIOD_COLUMN_NAME, OBS_VALUE_COLUMN_NAME


def get_data(identifier: str, target_currency: Optional[str] = None) -> pd.DataFrame:
    obs_value_x = "OBS_VALUE_x"
    obs_value_y = "OBS_VALUE_y"
    df = get_raw_data(identifier)

    if target_currency is not None:
        source_currency = identifier.split(".")[12]
        exchange_rates = get_exchange_rate(target_currency, source_currency)

        df = pd.merge(df, exchange_rates, on=TIME_PERIOD_COLUMN_NAME)
        df[OBS_VALUE_COLUMN_NAME] = df[obs_value_x] * df[obs_value_y]
        df.drop([obs_value_x, obs_value_y], axis=1, inplace=True)

    return df


data = get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP")

print("Data", data)
