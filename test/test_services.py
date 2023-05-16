import pytest
import pandas as pd

from api.services import _get_exchange_rate, _get_raw_data, _get_data, get_data, get_exchange_rate, get_raw_data
from fixture.test_services_fixture import IDENTIFIER, SOURCE_CURRENCY, TARGET_CURRENCY


@pytest.mark.asyncio
async def test_get_exchange_rate():
    source = SOURCE_CURRENCY
    target = TARGET_CURRENCY
    result = await _get_exchange_rate(source, target)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


@pytest.mark.asyncio
async def test_get_raw_data():
    identifier = IDENTIFIER
    result = await _get_raw_data(identifier)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


@pytest.mark.asyncio
async def test_get_data():
    identifier = IDENTIFIER
    target_currency = SOURCE_CURRENCY
    result = await _get_data(identifier, target_currency)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


def test_get_exchange_rate_sync():
    source = SOURCE_CURRENCY
    target = TARGET_CURRENCY
    result = get_exchange_rate(source, target)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


def test_get_raw_data_sync():
    identifier = IDENTIFIER
    result = get_raw_data(identifier)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


def test_get_data_sync():
    identifier = IDENTIFIER
    target_currency = SOURCE_CURRENCY
    result = get_data(identifier, target_currency)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
