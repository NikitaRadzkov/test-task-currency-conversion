import asyncio
from typing import Optional

import pandas as pd

from api.api_clients import EuropeanCentralBankClient
from api.constants import TIME_PERIOD_COLUMN_NAME, OBS_VALUE_COLUMN_NAME
from api.converters import EuropeanCentralBankXMLDataToDataFrameConverter


async def _get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:
    client = EuropeanCentralBankClient()
    data = await client.fetch_exchange_rate(source=source, target=target)
    converter = EuropeanCentralBankXMLDataToDataFrameConverter(data=data)
    return converter.process()


async def _get_raw_data(identifier: str) -> pd.DataFrame:
    client = EuropeanCentralBankClient()
    data = await client.fetch_raw_data(identifier=identifier)
    converter = EuropeanCentralBankXMLDataToDataFrameConverter(data=data)
    return converter.process()


async def _get_data(
        identifier: str,
        target_currency: Optional[str] = None,
) -> pd.DataFrame:
    source_currency = identifier.split('.')[12]
    needs_exchange = target_currency is not None
    coroutines = [_get_raw_data(identifier=identifier)]
    if needs_exchange:
        # switching target and source currencies as CEB has only rates with target EUR
        coroutines.append(_get_exchange_rate(source=target_currency, target=source_currency))
    raw_data, *others = await asyncio.gather(*coroutines)
    if needs_exchange:
        exchange_rate, *_ = others
        df = pd.merge(raw_data, exchange_rate, on=TIME_PERIOD_COLUMN_NAME, validate="1:1")
        left_column_name = f"{OBS_VALUE_COLUMN_NAME}_x"
        right_column_name = f"{OBS_VALUE_COLUMN_NAME}_y"
        df[OBS_VALUE_COLUMN_NAME] = df[left_column_name] * df[right_column_name]
        df = df.drop(columns=[left_column_name, right_column_name])
        return df

    return raw_data


def get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_get_exchange_rate(source=source, target=target),)


def get_raw_data(identifier: str) -> pd.DataFrame:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_get_raw_data(identifier=identifier),)


def get_data(
        identifier: str,
        target_currency: Optional[str] = None,
) -> pd.DataFrame:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_get_data(identifier=identifier, target_currency=target_currency),)
