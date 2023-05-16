import pandas as pd
from typing import Optional
from currency_conversion.get_raw_data import get_raw_data
from currency_conversion.get_exchange_rate import get_exchange_rate


def get_data(identifier: str, target_currency: Optional[str] = None) -> pd.DataFrame:
    df = get_raw_data(identifier)

    if target_currency is not None:
        source_currency = identifier.split(".")[12]
        exchange_rates = get_exchange_rate(target_currency, source_currency)

        df = pd.merge(df, exchange_rates, on="TIME_PERIOD")
        df["OBS_VALUE"] = df["OBS_VALUE_x"] * df["OBS_VALUE_y"]
        df.drop(["OBS_VALUE_x", "OBS_VALUE_y"], axis=1, inplace=True)
        df.rename(columns={"OBS_VALUE": "OBS_VALUE_IN_TARGET_CURRENCY"}, inplace=True)

    return df


data = get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP")

print("Data", data)
