import pandas as pd
import requests
import xml.etree.ElementTree as ElementTree


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
        data.append({"TIME_PERIOD": time_period, "OBS_VALUE": obs_value})

    df = pd.DataFrame(data)

    return df


data = get_exchange_rate("GBP")

print(data)
