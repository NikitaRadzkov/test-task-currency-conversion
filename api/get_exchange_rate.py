import pandas as pd
import requests
import xml.etree.ElementTree as ElementTree
from constants import TIME_PERIOD_COLUMN_NAME, OBS_VALUE_COLUMN_NAME


def get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:
    url = f"https://sdw-wsrest.ecb.europa.eu/service/data/EXR/M.{source}.{target}.SP00.A?detail=dataonly"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch exchange rate data. Status code: {response.status_code}")

    root = ElementTree.fromstring(response.content)

    data = []
    for obs in root.findall(".//generic:Obs",
                            namespaces={"generic": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"}):
        time_period = obs.find("./generic:ObsDimension", namespaces={
            "generic": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"}).attrib["value"]
        obs_value = float(obs.find("./generic:ObsValue", namespaces={
            "generic": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"}).attrib["value"])
        data.append({TIME_PERIOD_COLUMN_NAME: time_period, OBS_VALUE_COLUMN_NAME: obs_value})

    df = pd.DataFrame(data)

    return df


exchange_rate = get_exchange_rate("GBP")

print("Exchange Rate", exchange_rate)